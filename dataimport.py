#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import json
import datetime
import csv
from dateutil import parser
from datetime import datetime
from sni.models import *

# Clear out database
print("Begin deleting Quote")
qs = Quote.query.all()
for q in qs:
    db.session.delete(q)
    db.session.commit()
print("Finish deleting Quote")
print("Begin deleting QuoteCategory")
qcs = QuoteCategory.query.all()
for qc in qcs:
    db.session.delete(qc)
    db.session.commit()
print("Finish deleting QuoteCategory")
print("Begin deleting EmailThread")
ets = EmailThread.query.all()
for et in ets:
    db.session.delete(et)
    db.session.commit()
print("Finish deleting EmailThread")
print("Begin deleting Email")
Email.query.delete()
print("Finish deleting Email")
print("Begin deleting ForumThread")
fts = ForumThread.query.all()
for ft in fts:
    db.session.delete(ft)
    db.session.commit()
print("Finish deleting ForumThread")
print("Begin deleting Post")
Post.query.delete()
print("Finish deleting Post")
print("Begin deleting Category")
cats = Category.query.all()
for cat in cats:
    db.session.delete(cat)
    db.session.commit()
print("Finish deleting Category")
print("Begin deleting Format")
forms = Format.query.all()
for form in forms:
    db.session.delete(form)
    db.session.commit()
print("Finish deleting Format")
print("Begin deleting Author")
auths = Author.query.all()
for auth in auths:
    db.session.delete(auth)
    db.session.commit()
print("Finish deleting Author")
print("Begin deleting Doc")
Doc.query.delete()
print("Finish deleting Doc")
print("Begin deleting ResearchDoc")
ResearchDoc.query.delete()
print("Finish deleting ResearchDoc")
print("Begin deleting BlogPost")
BlogPost.query.delete()
print("Finish deleting BlogPost")
print("Begin deleting BlogSeries")
BlogSeries.query.delete()
print("Finish deleting BlogSeries")
print("Begin deleting Skeptic")
Skeptic.query.delete()
print("Finish deleting Skeptic")
print("Begin deleting Episode")
Episode.query.delete()
print("Finish deleting Episode")

# db.drop_all()
# db.create_all()


def get(model, **kwargs):
    return db.session.query(model).filter_by(**kwargs).first()


# See if object already exists for uniqueness
def get_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        return instance


print("Begin importing EmailThread")

with open('data/threads_emails.json') as data_file:
    threads = json.load(data_file)

for thread in threads:
    new_thread = EmailThread(
        id=thread['id'],
        title=thread['title'],
        source=thread['source']
    )
    db.session.add(new_thread)
    db.session.commit()

print("Finish importing ForumThread")
print("Begin importing Email")

with open('./data/emails.json') as data_file:
    emails = json.load(data_file)

for e in emails:
    satoshi_id = None
    if 'satoshi_id' in e.keys():
        satoshi_id = e['satoshi_id']
    parent = None
    if 'parent' in e.keys():
        parent = Email.query.get(e['parent'])
    new_email = Email(
        id=e['id'],
        satoshi_id=satoshi_id,
        url=e['url'],
        subject=e['subject'],
        sent_from=e['sender'],
        date=parser.parse(e['date']),
        text=e['text'],
        source=e['source'],
        source_id=e['source_id'],
        thread_id=e['thread_id'])
    if parent:
        new_email.parent = parent
    db.session.add(new_email)
    db.session.commit()

print("Finish importing Email")
print("Begin importing ForumThread")

with open('data/threads_forums.json') as data_file:
    threads = json.load(data_file)

for thread in threads:
    new_thread = ForumThread(
        id=thread['id'],
        title=thread['title'],
        url=thread['url'],
        source=thread['source']
    )
    db.session.add(new_thread)
    db.session.commit()

print("Finish importing ForumThread")
print("Begin importing Post")

with open('data/posts.json') as data_file:
    posts = json.load(data_file)

for i, p in enumerate(posts, start=1):
    satoshi_id = None
    if 'satoshi_id' in p.keys():
        satoshi_id = p['satoshi_id']
    post = Post(
        id=i,
        satoshi_id=satoshi_id,
        url=p['url'],
        subject=p['subject'],
        poster_name=p['name'],
        poster_url=p['poster_url'],
        post_num=p['post_num'],
        is_displayed=p['is_displayed'],
        nested_level=p['nested_level'],
        date=parser.parse(p['date']),
        text=p['content'],
        thread_id=p['thread_id']
    )
    db.session.add(post)
    db.session.commit()

print("Finish importing Post")
print("Begin importing QuoteCategory")

with open('./data/quotecategories.json') as data_file:
    quotecategories = json.load(data_file)

for qc in quotecategories:
    quote_category = QuoteCategory(
        slug=qc['slug'],
        name=qc['name']
    )
    db.session.add(quote_category)
    db.session.commit()

print("Finish importing QuoteCategory")
print("Begin importing Quote")

with open('./data/quotes.json') as data_file:
    quotes = json.load(data_file)

for i, quote in enumerate(quotes, start=1):
    q = Quote(
        id=i,
        text=quote['text'],
        date=parser.parse(quote['date']).date(),
        medium=quote['medium']
    )
    if 'email_id' in quote:
        q.email_id = quote['email_id']
    if 'post_id' in quote:
        q.post_id = quote['post_id']
    categories = []
    for cat in quote['category'].split(', '):
        categories += [get(QuoteCategory, slug=cat)]
    q.categories = categories
    db.session.add(q)
    db.session.commit()

print("Finish importing Quote")
print("Begin importing Author")

with open('./data/authors.json') as data_file:
    authors = json.load(data_file)

for i, author in enumerate(authors, start=1):
    author = Author(
        id=i,
        first=author['first'],
        middle=author['middle'],
        last=author['last'],
        slug=author['slug'])
    db.session.add(author)
    db.session.commit()

print("Finish importing Author")
print("Begin importing Doc")

with open('./data/literature.json') as data_file:
    docs = json.load(data_file)

for doc in docs:
    authorlist = doc['author']
    dbauthor = []
    for auth in authorlist:
        dbauthor += [get(Author, slug=auth)]
    formlist = doc['formats']
    dbformat = []
    for form in formlist:
        dbformat += [get_or_create(Format, name=form)]
    catlist = doc['categories']
    dbcat = []
    for cat in catlist:
        dbcat += [get_or_create(Category, name=cat)]
    if 'external' in doc:
        ext = doc['external']
    else:
        ext = None
    doc = Doc(
        id=doc['id'],
        title=doc['title'],
        author=dbauthor,
        date=doc['date'],
        slug=doc['slug'],
        formats=dbformat,
        categories=dbcat,
        doctype=doc['doctype'],
        external=ext)
    db.session.add(doc)
    db.session.commit()

print("Finish importing Doc")
print("Begin importing ResearchDoc")

with open('./data/research.json') as data_file:
    docs = json.load(data_file)

for doc in docs:
    authorlist = doc['author']
    dbauthor = []
    for auth in authorlist:
        dbauthor += [get(Author, slug=auth)]
    formlist = doc['formats']
    dbformat = []
    for form in formlist:
        dbformat += [get_or_create(Format, name=form)]
    catlist = doc['categories']
    dbcat = []
    for cat in catlist:
        dbcat += [get_or_create(Category, name=cat)]
    if 'external' in doc:
        ext = doc['external']
    else:
        ext = None
    if 'lit_id' in doc:
        lit = doc['lit_id']
    else:
        lit_id = None
    doc = ResearchDoc(
        id=doc['id'],
        title=doc['title'],
        author=dbauthor,
        date=doc['date'],
        slug=doc['slug'],
        formats=dbformat,
        categories=dbcat,
        doctype=doc['doctype'],
        external=ext,
        lit_id=lit)
    db.session.add(doc)
    db.session.commit()

print("Finish importing ResearchDoc")
print("Begin importing BlogSeries")
with open('./data/blogseries.json') as data_file:
    blogss = json.load(data_file)

for i, blogs in enumerate(blogss, start=1):
    blog_series = BlogSeries(
        id=i,
        title=blogs['title'],
        slug=blogs['slug'],
    )
    db.session.add(blog_series)
    db.session.commit()
print("Finish importing BlogSeries")
print("Begin importing BlogPost")

with open('./data/blogposts.json') as data_file:
    blogposts = json.load(data_file)

for i, bp in enumerate(blogposts, start=1):
    blogpost = BlogPost(
        id=i,
        title=bp['title'],
        author=[get(Author, slug=bp['author'])],
        date=parser.parse(bp['date']),
        added=parser.parse(bp['added']),
        slug=bp['slug'],
        excerpt=bp['excerpt'],
        languages=bp['languages'])
    try:
        blogpost.series = get(BlogSeries, slug=bp['series'])
        blogpost.series_index = bp['series_index']
    except KeyError:
        pass
    db.session.add(blogpost)
    db.session.commit()

print("Finish importing ResearchDoc")
print("Begin importing Skeptic")

with open('./data/skeptics.json') as data_file:
    skeptics = json.load(data_file)

for i, skeptic in enumerate(skeptics, start=1):
    slug_date = datetime.strftime(parser.parse(skeptic['date']), '%Y-%m-%d')
    skeptic = Skeptic(
        id=i,
        name=skeptic['name'],
        title=skeptic['title'],
        article=skeptic['article'],
        date=parser.parse(skeptic['date']),
        source=skeptic['source'],
        excerpt=skeptic['excerpt'],
        price=skeptic['price'],
        link=skeptic['link'],
        waybacklink=skeptic['waybacklink'],
        slug='{}-{}'.format(skeptic['slug'], slug_date)
    )
    db.session.add(skeptic)
    db.session.commit()

print("Finish importing Skeptic")
print("Begin importing Episode")

with open('./data/episodes.json') as data_file:
    episodes = json.load(data_file)

for ep in episodes:
    episode = Episode(
        id=ep['id'],
        title=ep['title'],
        date=parser.parse(ep['date']),
        duration=ep['duration'],
        subtitle=ep['subtitle'],
        summary=ep['summary'],
        slug=ep['slug'],
        youtube=ep['youtube'],
        address=ep['address'],
        time=parser.parse(ep['time']))
    db.session.add(episode)
    db.session.commit()

print("Finish importing Episode")
