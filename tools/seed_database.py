from utilities.models import *


@db_session
def seed_database_url():
    urls = [
        "https://thehiddenwiki.org/"
    ]
    for u in urls:
        url = Url(
            url=u,
            date_added=datetime.now()
        )

@db_session
def seed_database_keyword():
    keywords = [
        "hack",
        "bankdrop",
        "exploit",
        "deloite"
    ]
    for k in keywords:
        keyword = Keyword(
            keyword=k,
            active=True
        )


if __name__ == "__main__":
    print("Seeding database with urls...")
    seed_database_url()
    print("Seeding database with keyword...")
    seed_database_keyword()
