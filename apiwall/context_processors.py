import mistune

def utility_processor():

    def render_markdown(content):
        if content:
            markdown = mistune.Markdown()
            return markdown(content)

    return dict(render_markdown=render_markdown)
