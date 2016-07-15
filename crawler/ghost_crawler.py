import ghost

g = ghost.Ghost()
with g.start() as session:
    page, extra_resources = session.open("https://www.debian.org")
    if page.http_status == 200 and \
            'The Universal Operating System' in page.content:
        print("Good!")