from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, not_
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class Articles(db.Model):
    title: Mapped[str] = mapped_column()
    article_link: Mapped[str] = mapped_column(primary_key=True)
    source_logo: Mapped[str] = mapped_column()
    source_name: Mapped[str] = mapped_column()
    preview_image: Mapped[str] = mapped_column()
    publication_date: Mapped[datetime] = mapped_column()
    article_content: Mapped[str] = mapped_column()
    tag_list: Mapped[str] = mapped_column()
    view_count: Mapped[int] = mapped_column()
    like_amount: Mapped[int] = mapped_column()
    dislike_amount: Mapped[int] = mapped_column()

    def jsonify(self):
        result = {
            'title': self.title,
            'article_link': self.article_link,
            'source_logo': self.source_logo,
            'source_name': self.source_name,
            'preview_image': self.preview_image,
            'publication_date': self.publication_date.strftime("%a, %d %b %Y %H:%M:%S"),
            'tag_list': (self.tag_list[2:-2]).split("', '"),
            'view_count': self.view_count,
        }

        return result


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_aggregator.db'

db.init_app(app)

page_length = 10


@app.route('/news_aggregator/api/article_list/popular', methods=['POST'])
def get_popular():  # put application's code here

    print(request.form)

    result = db.session.query(Articles).order_by(Articles.view_count.desc())
    next_page_identifier = int(request.values["next_page_identifier"])

    if request.values['time_period'] != '':
        time_period = float(request.values["time_period"])  # days
        result = result.filter(Articles.publication_date >= datetime.utcnow() - timedelta(days=time_period))

    result = result.limit(page_length * (next_page_identifier + 1)).offset(next_page_identifier * page_length).all()

    next_page_identifier = None if result == [] else next_page_identifier+1

    response = {'articles': [], 'next_page_identifier': next_page_identifier}

    for i in result:
        response['articles'].append(i.jsonify())

    # print(json.dumps(response, sort_keys=True, indent=4))

    return jsonify(response)


@app.route('/news_aggregator/api/article_list/recommended', methods=['POST'])
def get_recommended():  # put application's code here

    next_page_identifier = int(request.values["next_page_identifier"])
    preferred_tags = request.values["preferred_tags"].split(",")
    banned_tags = request.values["banned_tags"].split(",")

    preferred = [Articles.tag_list.ilike(f'%{tag}%') for tag in preferred_tags] if request.values[
                                                                                       "preferred_tags"] != "" else []
    banned = [Articles.tag_list.notilike(f'%{tag}%') for tag in banned_tags] if request.values[
                                                                                    "banned_tags"] != "" else []

    result = db.session.query(Articles).order_by(Articles.publication_date.desc()) \
        .filter(and_(or_(*preferred), and_(*banned))) \
        .limit(page_length * (next_page_identifier + 1)).offset(next_page_identifier * page_length).all()

    next_page_identifier = None if result == [] else next_page_identifier + 1

    response = {'articles': [], 'next_page_identifier': next_page_identifier}

    for i in result:
        response['articles'].append({
            'title': i.title,
            'article_link': i.article_link,
            'source_logo': i.source_logo,
            'source_name': i.source_name,
            'preview_image': i.preview_image,
            'publication_date': i.publication_date.strftime("%a, %d %b %Y %H:%M:%S"),
            'tag_list': (i.tag_list[2:-2]).split("', '"),
            'view_count': i.view_count,
        })

    return jsonify(response)


@app.route('/news_aggregator/api/article_content', methods=['GET'])
def get_content():  # put application's code here

    link = request.values['link']

    print(link)

    try:
        result = db.session.query(Articles).filter(Articles.article_link == link).first().article_content

    except:
        print("Статья отстутствует")
        result = None

    return jsonify(result)


@app.route('/news_aggregator/api/update_views', methods=['GET'])
def update_views():  # put application's code here

    link = request.values['link']

    try:
        result = db.session.query(Articles).filter(Articles.article_link == link).first()
        result.view_count += 1
        db.session.commit()
    except:
        print("Статья отстутствует")
        result = None

    return 'updated'


if __name__ == '__main__':
    app.run(use_reloader=True, threaded=True)
