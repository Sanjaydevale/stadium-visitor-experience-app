import database
import vistors
class Visit:
    food = ["noodles", "pizza", "burger", "french fries", "pepsi"]
    rooms = {1 : ["A/C",1000], 2 : ["non A/C", 600]}
    def __init__(self, name, password, room = "", food = []) -> None:
        # validate the user
        user = vistors.Vistor.get_user(name)
        user_data = user.user_details()
        if password != user_data["password"]:
            print("invalid name or password")
            return
        self.user = user
        self.name = name
        self.data = {
            "user" : user.user_details(),
            "room" : room,
            "food" : food,
        }

        self.__create_visit()
        # if the usre is valid provide visit sevices

    def __create_visit(self):
        db = database.JsonDB("data.json")
        data = db.read("visits")
        if data == None:
            db.create({"visits" : {}})
        data = db.read("visits")
        data["visits"].update({self.data["user"]["name"]: self.data})
        db.update("visits", data)
        db.save_data()

    def save_visit(self):
        db = database.JsonDB("data.json")
        data = db.read("visits")
        data["visits"].update({self.data["user"]["name"]: self.data})
        db.update("visits", data)
        db.save_data()

    def delete_visit(self):
        db = database.JsonDB("data.json")
        data = db.read("visits")
        data["visits"].pop(self.data["user"]["name"])
        db.update("visits", data)
        db.save_data()
    
    def visit_details(self):
        return self.data
    
    def order_food(self):
        prev_order = self.data["user"]["orders"]
        if len(prev_order) > 0:
            print(f"suggested items : {max(set(prev_order), key = prev_order.count)}")
        for i in range(len(self.food)):
            print(f"{i+1} : {self.food[i]}")
        food_id = int(input("enter food id : ")) - 1
        self.data["food"] += [self.food[food_id]]
        self.user.update_orders(self.food[food_id])
        self.user = vistors.Vistor.get_user(self.name)
        self.data["user"] = self.user.user_details()
        self.save_visit()

    def book_room(self):

        for key, val in self.rooms.items():
            print(f"{key} : {val[0]}, cost = {val[1]}")
        room = int(input("enter room id : ")) 
        print(f"room booked f{self.rooms[room]}")
        self.data["room"] = room
        self.save_visit()

    @staticmethod
    def get_visit(name, password):
        db = database.JsonDB("data.json")
        data = db.read("visits")
        if data == None:
            return Visit(name, password)
        if name not in data["visits"].keys():
            print(f"no visitor named {name}")
            return None
        visit_data = data["visits"][name]
        return Visit(name, password, visit_data["room"], visit_data["food"])

