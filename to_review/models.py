class AssetData:
    address: str
    link: str
    name: str
    category: str
    website: str
    description: str

    def __init__(self, address: str, link: str, name: str, category: str, website: str, description: str):
        self.address = address
        self.link = link
        self.name = name
        self.category = category
        self.website = website
        self.description = description