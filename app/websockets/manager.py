class ConnectionManager:
    def __init__(self):
        # 👇 aquí guardamos conexiones por tipo
        self.admins = []

    async def connect(self, websocket, role_id: int):
        await websocket.accept()

        if role_id == 1:
            self.admins.append(websocket)

    def disconnect(self, websocket):
        if websocket in self.admins:
            self.admins.remove(websocket)

    async def send_to_admins(self, message: dict):
        for conn in self.admins:
            await conn.send_json(message)


# 👇 instancia global
manager = ConnectionManager()