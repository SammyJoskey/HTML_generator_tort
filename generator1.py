class Tag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        
        self.tag = tag
        self.is_single = is_single
        self.text = ""
        self.attributes = {}
        self.subtag = ""
                        
        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value

        attrs = []
        for attribute, value in self.attributes.items():
            if "_" in attribute:
                attribute = attribute.replace("_", "-")
            attrs.append('{}="{}"'.format(attribute, value))
        self.attrs = " ".join(attrs)
        if self.attrs != "":
            self.attrs = " " + self.attrs

     
    def __enter__(self):
        return self

    def __str__(self, *args):

        self.opening = f"<{self.tag}{self.attrs}>{self.text}"
        self.closing = f"</{self.tag}>"
        if self.is_single:
            return self.opening
        elif self.tag == "p" or self.tag == "title" or self.tag == "h1":
            return self.opening + self.subtag + self.closing
        else:
            return self.opening + self.subtag + "\n" + self.closing
        
    def __iadd__(self, other):
                
        self.subtag += ("\n" + str(other))
        return Tag(self.tag, is_single=False, subtag = self.subtag, **kwargs)


    def __exit__(self, *args):
        return self

class HTML(Tag):

    def __init__(self, output="None"):

        self.output = output
        self.tag = "html"
        self.attrs = ""
        self.text = ""
        self.is_single=False
        self.subtag = ""

    def __exit__(self, *args):
    
        if self.output == "None":
            print(self)
            return self
        else:
            print(f"saving to file {self.output}")
            file_object = open(self.output, "w", encoding = "utf-8")
            file_object.write(str(self))
            file_object.close()
            return self
    
class TopLevelTag(Tag):
    is_single=False

def main(output=None):
    with HTML(output=output) as doc: 
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body

if __name__ == "__main__":
    main('text.html')