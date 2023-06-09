#
# from flask_socketio import SocketIO, emit
# from flask import Blueprint
# from main import mobile
#
# socketio = SocketIO(mobile, async_mode='gevent')
#
# mod = Blueprint('socketio_routes', __name__)
#
# @socketio.on('connect')
# def handle_connect():
#     emit('connected', {'data': 'Connected'})
#
# @socketio.on("join-room")
# def on_join_room(data):
#     sid = request.sid
#     room_id = data["room_id"]
#     display_name = session[room_id]["name"]
#
#     # register sid to the room
#     join_room(room_id)
#     rooms_sid[sid] = room_id
#     names_sid[sid] = display_name
#
#     # broadcast to others in the room
#     print("[{}] New member joined: {}<{}>".format(room_id, display_name, sid))
#     emit("user-connect", {"sid": sid, "name": display_name},
#          broadcast=True, include_self=False, room=room_id)
#
#     # add to user list maintained on server
#     if room_id not in users_in_room:
#         users_in_room[room_id] = [sid]
#         emit("user-list", {"my_id": sid})  # send own id only
#     else:
#         usrlist = {u_id: names_sid[u_id]
#                    for u_id in users_in_room[room_id]}
#         # send list of existing users to the new member
#         emit("user-list", {"list": usrlist, "my_id": sid})
#         # add new member to user list maintained on server
#         users_in_room[room_id].append(sid)
#
#     print("\nusers: ", users_in_room, "\n")
#
#
# @socketio.on("disconnect")
# def on_disconnect():
#     sid = request.sid
#     room_id = rooms_sid[sid]
#     display_name = names_sid[sid]
#
#     print("[{}] Member left: {}<{}>".format(room_id, display_name, sid))
#     emit("user-disconnect", {"sid": sid},
#          broadcast=True, include_self=False, room=room_id)
#
#     users_in_room[room_id].remove(sid)
#     if len(users_in_room[room_id]) == 0:
#         users_in_room.pop(room_id)
#
#     rooms_sid.pop(sid)
#     names_sid.pop(sid)
#
#     print("\nusers: ", users_in_room, "\n")
#
#
# @socketio.on("data")
# def on_data(data):
#     sender_sid = data['sender_id']
#     target_sid = data['target_id']
#     if sender_sid != request.sid:
#         print("[Not supposed to happen!] request.sid and sender_id don't match!!!")
#
#     if data["type"] != "new-ice-candidate":
#         print('{} message from {} to {}'.format(
#             data["type"], sender_sid, target_sid))
#     socketio.emit('data', data, room=target_sid)