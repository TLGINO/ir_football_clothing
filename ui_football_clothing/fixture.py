import json


class Fixture:
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.create_fixture()

    def create_fixture(self):
        i = 0
        all_data = []
        for file_path in self.file_paths:
            for data in json.load(open(file_path)):
                i += 1

                template = {
                    "model": "ui_football_clothing.item",
                    "pk": i,
                    "fields": {
                        "url": data["url"],
                        "title": data["title"],
                        "data": data["data"],
                        "price": data["price"],
                        "image": data["image"],
                    },
                }
                all_data.append(template)

        json.dump(all_data, open("ui_football_clothing/fixtures/data.json", "w+"))
        print("Fixtures data created successfully")


if __name__ == "__main__":
    file_paths = [
        "../data/adidas.json",
        "../data/decathlon.json",
        "../data/sports_direct.json",
    ]
    fixture = Fixture(file_paths)
