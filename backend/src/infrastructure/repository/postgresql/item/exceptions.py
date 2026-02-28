class NFException(Exception):
    def __init__(self, item_id: int) -> None:
        super().__init__(f"Item : id={item_id} not found.")
        self.item_id = item_id
