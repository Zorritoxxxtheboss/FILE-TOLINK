import aiohttp
import aiohttp_socks
import asyncio
import json
import os
import pymegatools
import re
import requests
import shutil
import yt_dlp

import mediafire_dl
from io import BufferedReader
from json import loads
from multivolumefile import MultiVolume
from moodle_client import MoodleClient2
from rev_client import RevClient
from os import unlink
from os.path import exists
from pathlib import Path
from py7zr import FILTER_COPY, SevenZipFile
from pyrogram import Client, filters
from pyrogram.types import Message
from random import randint
from re import findall
from time import localtime, time
from urllib.parse import quote, quote_plus, unquote_plus
from zipfile import ZipFile

api_id = 9652234
api_hash = "e532d52554115eed48f82f7dcb10b171"
bot_token = "7230367967:AAFI14nore-QOEb9hOuk88wN-LWB5zphNuE"

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
boss = 'zorritotheboss'  # usuarios supremos

Configs = {"uclv": '', "gtm": "", "uvs": "", "ltu": "", "uccfd": "", "vcl": "",
           "ucuser": "", "ucpass": "", "uclv_p": "", "gp": None, "s": "On",
           'zorritotheboss': {'z': 99, "m": "e", "a": "c", "t": "y", "gp": False},
           }

Urls = {}  # urls subidos a educa
Urls_draft = {}  # urls para borrar de draft
Config = {}  # configuraciones privadas de moodle
id_de_ms = {}  # id de mensage a borrar con la funcion de cancelar
root = {}  # directorio actual
downlist = {}  # lista de archivos descargados
procesos = 0  # numero de procesos activos en el bot
save_cred = {"mariali.guzman": {"ID": None, "TOKEN": "Nxc7adpadCttdZc"}}
control_upload = {}
bytes_control = {}
save_c = {"user": "", "passw": ""}
TEMP_FILE = {}
# total en gb o megas subidos en bytes (int)
total_up = {'zorritotheboss': {'P': 0, 'S': 0}}
rvs = {'zorritotheboss': {'h': '', 'u': '', 'p': '', 'up': '', 'z': 0, 'm': 'm'}}

# inicio
@bot.on_message(filters.command("start", prefixes="/") & filters.private)
async def start(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
 
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id=boss, text=intento_msg)
		return
	zipps = str(Configs[username]["z"])
	auto = Configs[username]["t"]
	total = shutil.disk_usage(os.getcwd())[0]
	used = shutil.disk_usage(os.getcwd())[1]
	free = shutil.disk_usage(os.getcwd())[2]	

	a = await client.send_message(username,'**🔎 Buscando Datos**')
	msg = f"✧ 𝐁𝐨𝐭 𝐂𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧\n"
	msg += f"➣𝘡𝘪𝘱𝘴 𝘤𝘰𝘯𝘧𝘪𝘨𝘶𝘳𝘢𝘥𝘰𝘴 𝘢: **{zipps}MB**\n"	    
	msg += "➣𝘌𝘴𝘵𝘢𝘥𝘰 𝘥𝘦𝘭 𝘣𝘰𝘵: "+ Configs["s"] +"\n"
	if auto == "y":
		msg += "➣𝘈𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤 𝘜𝘱: **On**\n\n"
	else:
		msg += "➣𝘈𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤 𝘜𝘱: **Off**\n\n"
	if Configs[username]["a"] == "j":
		mode = "➣𝘌𝘥𝘶𝘤𝘢 ➥ **Directs Links**\n"
	elif Configs[username]["a"] == "c":
		mode = "➣𝘜𝘤𝘭𝘷 ➥ **Directs Links (Calendar)**\n"
	elif Configs[username]["a"] == "d":
		mode = "➣𝘗𝘦𝘳𝘴𝘰𝘯𝘢𝘭 𝘤𝘭𝘰𝘶𝘥 ➥ **Draft Links**\n\n"
	elif Configs[username]["a"] == "a":
		mode = "➣𝘜𝘤𝘭𝘷 ➥ **Directs Links (Procfile)**\n\n"
	else:
		mode = "➣NEXTCLOUD➥ **Directs Links**\n\n"
##        msg += "𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨\n"
##        msg += f"➣𝘚𝘺𝘴𝘵𝘦𝘮: **{uname.system}**\n"
##        msg += f"➣𝘔𝘢𝘤𝘩𝘪𝘯𝘦: **{uname.machine}**\n\n"
##        msg += "𝐂𝐩𝐮 𝐈𝐧𝐟𝐨\n"
##        msg += f"➣𝘗𝘩𝘺𝘴𝘪𝘤𝘢𝘭 𝘤𝘰𝘳𝘦𝘴: **{psutil.cpu_count(logical=False)}**"
##        msg += f"\n➣𝘛𝘰𝘵𝘢𝘭 𝘤𝘰𝘳𝘦𝘴: **{psutil.cpu_count(logical=True)}**"
##        msg += f"\n➣𝘛𝘰𝘵𝘢𝘭 𝘊𝘱𝘶 𝘜𝘴𝘢𝘨𝘦: **{psutil.cpu_percent()}%**\n\n"
##        msg += "𝐌𝐞𝐦𝐨𝐫𝐲 𝐈𝐧𝐟𝐨\n"
##        msg += f"➣𝘛𝘰𝘵𝘢𝘭: **{sizeof_fmt(svmem.total)}**\n"
##        msg += f"➣𝘍𝘳𝘦𝘦: **{sizeof_fmt(svmem.available)}**\n"
##        msg += f"➣𝘜𝘴𝘦𝘥: **{sizeof_fmt(svmem.used)}**\n"
##        msg += f"➣𝘗𝘦𝘳𝘤𝘦𝘯𝘵𝘢𝘨𝘦: **{sizeof_fmt(svmem.percent)}%**\n\n"
	msg += f"𝐃𝐢𝐬𝐤 𝐈𝐧𝐟𝐨\n"
	msg += f"➣𝘛𝘰𝘵𝘢𝘭 𝘴𝘵𝘰𝘳𝘢𝘨𝘦: **{sizeof_fmt(used)}** / **{sizeof_fmt(total)}**\n"
	msg += f"➣𝘍𝘳𝘦𝘦 𝘴𝘵𝘰𝘳𝘢𝘨𝘦: **{sizeof_fmt(free)}**\n\n"
        
	msg += mode
	await a.edit(msg)
# modos de subida y config
@bot.on_message(filters.command("educa", prefixes="/")& filters.private)
async def educa(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["m"] = "e"
	Configs[username]["a"] = "j"
	Configs[username]["z"] = 999

	await send("☁️ Nube Educa Activada ☁️")

@bot.on_message(filters.command("uclv", prefixes="/")& filters.private)
async def uclv(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "c"
	Configs[username]["z"] = 399

	await send("☁️ Uclv Activada ☁️")

@bot.on_message(filters.command("cloud", prefixes="/")& filters.private)
async def cloud(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["m"] = "d"
	Configs[username]["a"] = "d"
	Configs[username]["z"] = 99

	await send("☁️ Subida a Draft Activada ☁️")

@bot.on_message(filters.command("perfil_my", prefixes="/")& filters.private)
async def perfil_my(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "a"
	Configs[username]["z"] =  399

	await send("☁️ Perfil_my Activada ☁️")
 #Agragdo reciente   
@bot.on_message(filters.command("set_uo", prefixes="/")& filters.private)
async def set_uo(client: Client, message:Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	if save_c["user"]!="":
		Configs[username]["m"] = "n"
		Configs[username]["a"] = "z"
		Configs[username]["z"] = 99
		Config[username]["username"] = save_c["user"]
		Config[username]["password"] = save_c["passw"]
		Config[username]["host"] = "https://nube.uo.edu.cu/"
		Config[username]["repoid"] = 4
	
		await send("✅ 𝑫𝒐𝒏𝒆\nNube Activada...")
	else:
		await bot.send_message(username,"No hay ninguna nube confurada..")
 #Agragdo reciente       
@bot.on_message(filters.command("set", prefixes="/")& filters.private)
async def set_uo(client: Client, message:Message):
	username = message.from_user.username
	send = message.reply
	if username in boss:
		data = message.text.split(" ")
		user = data[1]
		passw = data[2]
		save_c["user"] = user
		save_c["passw"] = passw
		await send("✅ 𝑫𝒐𝒏𝒆\nNube Activada...")

@bot.on_message(filters.command("uvs_ucm", prefixes="/")& filters.private)
async def uvs_ucm(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "b"
	Configs[username]["z"] = 100

	await send("☁️ Nube uvs_ucm Activada ☁️")

@bot.on_message(filters.command("aula_gtm", prefixes="/")& filters.private)
async def aula_gtm(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "h"
	Configs[username]["z"] = 7

	await send("☁️ Nube gtm Activada ☁️")

@bot.on_message(filters.command("uvs_ltu", prefixes="/")& filters.private)
async def uvs_ltu(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "l"
	Configs[username]["z"] = 100

	await send("☁️ Uvs_ltu Activada ☁️")

@bot.on_message(filters.command("aula_vcl", prefixes="/")& filters.private)
async def aula_vcl(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "v"
	Configs[username]["z"] = 50

	await send("☁️ Aula_vcl Activada ☁️")

@bot.on_message(filters.command("uccfd", prefixes="/")& filters.private)
async def uccfd(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "u"
	Configs[username]["z"] = 5

	await send("☁️ Nube uccfd Activada ☁️")	

@bot.on_message(filters.command("perfil", prefixes="/")& filters.private)
async def perfil(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "t"
	Configs[username]["z"] = 399

	await send("✅ Operacion Realizada ✅")
#Agragdo recient


@bot.on_message(filters.command("status", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	host = Config[username]["host"]
	proxy = Configs[username]["gp"]
	if proxy:
		proxy = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
	else:
		proxy = aiohttp.TCPConnector()
	msg = await send("📡 __Conectando [...]__")
	async with aiohttp.ClientSession(connector=proxy) as session:
		inicio = time()
		async with session.get(host+"login") as response:
			status_code = response.status
			ms = str((time() - inicio) * 1000)[:4]
			if status_code==200:
				await msg.edit(f"✅ `{host}`\n\n🏷 Status: {status_code}\n🎟 Ping: {ms} ms")
			else:
				await msg.edit(f"❌ `{host}`\n\n🏷 Status: {status_code}\n🎟 Ping: {ms} ms")


@bot.on_message(filters.command("config", prefixes="/")& filters.private)
async def config(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	cuenta = message.text
	host = message.text.split(" ")[1]
	user = message.text.split(" ")[2]
	password = message.text.split(" ")[3]
	repoid = message.text.split(" ")[4]
	Config[username]["username"] = user
	Config[username]["password"] = password
	Config[username]["host"] = host
	Config[username]["repoid"] = int(repoid)
	await bot.send_message(boss, f"#Cuentas\n\n{cuenta}")
	await send("✅ Operacion Realizada ✅")

@bot.on_message(filters.command("zips", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	sip = int(message.text.split(" ")[1])
	Configs[username]["z"] = sip

	await send("✅ Operacion Realizada ✅")

@bot.on_message(filters.command("Global", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		sip = "socks5://" +message.text.split(" ")[1]
		Configs["gp"] = sip
	
		await send("✅ Proxy Global Activado")
	else:return

@bot.on_message(filters.command("proxy", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	sip = "socks5://" +message.text.split(" ")[1]
	Configs[username]["gp"] = sip

	await send("🚀 Proxy Personal Activado 🚀")

@bot.on_message(filters.command("proxyoff", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	Configs[username]["gp"] = False

	await send("✖️ Proxy Personal Desactivado ✖️")

@bot.on_message(filters.command("token_uvs", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		sip = message.text.split(" ")[1]
		Configs["uvs"] = sip
	
		await send("✅ Operacion Realizada ✅")
	else:return

@bot.on_message(filters.command("token_gtm", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		sip = message.text.split(" ")[1]
		Configs["gtm"] = sip
	
		await send("✅ Operacion Realizada ✅")
	else:return

@bot.on_message(filters.command("token_ltu", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		sip = message.text.split(" ")[1]
		Configs["ltu"] = sip
	
		await send("✅ Operacion Realizada ✅")
	else:return

@bot.on_message(filters.command("token_uclv", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		sip = message.text.split(" ")[1]
		Configs["uclv"] = sip
	
		await send("✅ Operacion Realizada ✅")
	else:return

@bot.on_message(filters.command("token_vcl", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		sip = message.text.split(" ")[1]
		Configs["vcl"] = sip
	
		await send("✅ Token vcl activado")
	else:return

@bot.on_message(filters.command("token_uccfd", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		sip = message.text.split(" ")[1]
		Configs["uccfd"] = sip
	
		await send("✅ Token uccfd activado")
	else:return

@bot.on_message(filters.command("offglobal", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		Configs["gp"] = False
	
		await send("✖️ Proxy Global off ✖️")
	else:return


#descargas
@bot.on_message(filters.command("download", prefixes="/")& filters.private)
async def download_archive(client: Client, message: Message):
	global procesos
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	comp = comprobar_solo_un_proceso(username) 
	if comp != False:
		await send(comp)
		return
	total_proc = total_de_procesos()
	if total_proc != False:
		await send(total_proc)
		return
	procesos += 1
	msg = await send("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
	count = 0
	for i in downlist[username]:
		filesize = int(str(i).split('"file_size":')[1].split(",")[0])
		try:
			filename = str(i).split('"file_name": ')[1].split(",")[0].replace('"',"")	
		except:
			filename = str(randint(11111,999999))+".mp4"
		await bot.send_message(boss, f'**@{username} Envio un #archivo:**\n**Filename:** {filename}\n**Size:** {sizeof_fmt(filesize)}')	
		start = time()
		try:
			await msg.edit(f"𝑷𝒓𝒆𝒑𝒂𝒓𝒂𝒏𝒅𝒐 𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂\n\n`{filename}`")
		except:
			break
		try:
			a = await i.download(file_name=str(root[username]["actual_root"])+"/"+filename,progress=downloadmessage_progres,progress_args=(filename,start,msg))
			if Path(str(root[username]["actual_root"])+"/"+ filename).stat().st_size == filesize:
				await msg.edit("𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂 𝒆𝒙𝒊𝒕𝒐𝒔𝒂")
				count +=1
		except Exception as ex:
			if procesos > 0:
				procesos -= 1
			if "MessageIdInvalid" in str(ex):
				pass
			else:
				#await bot.send_message(username,ex)
				return
	if count == len(downlist[username]):
		if count == 0:
			return
		if procesos > 0:
			procesos -= 1
		await msg.edit("𝑻𝒐𝒅𝒐𝒔 𝒍𝒐𝒔 𝒂𝒓𝒄𝒉𝒊𝒗𝒐𝒔 𝒉𝒂𝒏 𝒔𝒊𝒅𝒐 𝒅𝒆𝒔𝒄𝒂𝒓𝒈𝒂𝒅𝒐𝒔")
		downlist[username] = []
		count = 0
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		return
	else:
		await msg.edit("**Error**")
		if procesos > 0:
			procesos -= 1
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		downlist[username] = []
		return		

#root
@bot.on_message(filters.command("rm", prefixes="/")& filters.private)
async def rm(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	list = message.text.split(" ")[1]	
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	if "-" in list:
		v1 = int(list.split("-")[-2])
		v2 = int(list.split("-")[-1])
		for i in range(v1,v2+1):
			try:
				unlink(str(root[username]["actual_root"])+"/"+msgh[1][i])
			except Exception as ex:
				await bot.send_message(username,ex)
		msg = files_formatter(str(root[username]["actual_root"])+"/",username)
		await limite_msg(msg[0],username)
	else:
		try:
			unlink(str(root[username]["actual_root"])+"/"+msgh[1][int(list)])
			msg = files_formatter(str(root[username]["actual_root"])+"/",username)
			await limite_msg(msg[0],username)
		except Exception as ex:
			await bot.send_message(username,ex)

@bot.on_message(filters.command("rmdir", prefixes="/")& filters.private)
async def rmdir(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	list = message.text.split(" ")[1]	
	filespath = Path(str(root[username]["actual_root"])+"/")
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	try:
		shutil.rmtree(str(root[username]["actual_root"])+"/"+msgh[1][int(list)])
		msg = files_formatter(str(root[username]["actual_root"])+"/",username)
		await limite_msg(msg[0],username)
	except Exception as ex:
		await bot.send_message(username,ex)

@bot.on_message(filters.command("deleteall", prefixes="/")& filters.private)
async def delete_all(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	shutil.rmtree("downloads/"+username+"/")
	root[username]["actual_root"] = "downloads/"+username
	msg = files_formatter(str(root[username]["actual_root"])+"/",username)
	await limite_msg(msg[0],username)

@bot.on_message(filters.command("seven", prefixes="/")& filters.private)
async def seven(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	lista = message.text.split(" ")
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	if len(lista) == 2:
		i = int(lista[1])
		j = str(msgh[1][i])
		if not "." in j:
			h = await send(f"𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
			g = str(root[username]["actual_root"]+"/")+msgh[1][i]
			p = shutil.make_archive(j, format = "zip", root_dir=g)
			await h.delete()
			shutil.move(p,root[username]["actual_root"])	
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			return
		else:
			g = str(root[username]["actual_root"]+"/")+msgh[1][i]
			o = await send("𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
			a = filezip(g,volume=None)
			await o.delete()
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			return

	elif len(lista) == 3:
		i = int(lista[1])
		j = str(msgh[1][i])
		t = int(lista[2])
		g = str(root[username]["actual_root"]+"/")+msgh[1][i]
		h = await send(f"𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
		if not "." in j:
			p = shutil.make_archive(j, format = "zip", root_dir=g)
			await h.edit("𝑫𝒊𝒗𝒊𝒅𝒊𝒆𝒏𝒅𝒐 𝒆𝒏 𝒑𝒂𝒓𝒕𝒆𝒔")
			a = sevenzip(p,password=None,volume = t*1024*1024)
			os.remove(p)
			for i in a :
				shutil.move(i,root[username]["actual_root"])
			await h.edit("𝑪𝒐𝒎𝒑𝒓𝒆𝒔𝒊𝒐𝒏 𝒓𝒆𝒂𝒍𝒊𝒛𝒂𝒅𝒂")
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			return
		else:
			a = sevenzip(g,password=None,volume = t*1024*1024)
			await h.edit("𝑪𝒐𝒎𝒑𝒓𝒆𝒔𝒊𝒐𝒏 𝒓𝒆𝒂𝒍𝒊𝒛𝒂𝒅𝒂")
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			return

@bot.on_message(filters.command("unzip", prefixes="/")& filters.private)
async def unzip(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	archivo = message.text.split(" ")[1]
	ruta = str(root[username]["actual_root"])
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	archivor = str(root[username]["actual_root"])+"/"+msgh[1][int(archivo)]
	a = await send("𝑫𝒆𝒔𝒄𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐 𝒂𝒓𝒄𝒉𝒊𝒗𝒐")
	try:
		descomprimir(archivor,ruta)
		await a.edit("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝒅𝒆𝒔𝒄𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒅𝒐")
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		return
	except Exception as ex:
		await a.edit("Error: ",ex)
		return

@bot.on_message(filters.command("mkdir", prefixes="/")& filters.private)
async def mkdir(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	name = message.text.split(" ")[1]
	if "." in name or "/" in name or "*" in name:
		await send("💢𝑬𝒍 𝒏𝒐𝒎𝒃𝒓𝒆 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆 𝒄𝒐𝒏𝒕𝒆𝒏𝒆𝒓 . , * /")
		return
	rut = root[username]["actual_root"]
	os.mkdir(f"{rut}/{name}")
	await send(f"𝙎𝙚 𝙘𝙧𝙚𝙤 𝙡𝙖 𝙘𝙖𝙧𝙥𝙚𝙩𝙖\n\n /{name}")
	msg = files_formatter(str(root[username]["actual_root"]),username)
	await limite_msg(msg[0],username)

@bot.on_message(filters.command("mv", prefixes="/")& filters.private)
async def mv(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	lista = message.text.split(" ")
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	new_dir = int(lista[2])
	new = str(root[username]["actual_root"]+"/")+msgh[1][new_dir]
		
	if "-" in lista[1]:
		actual = lista[1]
		v1 = int(actual.split("-")[-2])
		v2 = int(actual.split("-")[-1])
		for i in range(v1,v2+1):
			try:
				actual = str(root[username]["actual_root"]+"/")+msgh[1][i]	
				shutil.move(actual,new)
			except Exception as ex:
				await bot.send_message(username,ex)
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		return
	else:
		actual_dir = int(lista[1])
		try:
			actual = str(root[username]["actual_root"]+"/")+msgh[1][actual_dir]
			k = actual.split("downloads/")[-1]
			t = new.split("downloads/")[-1]
			await send(f"𝑴𝒐𝒗𝒊𝒅𝒐 𝒄𝒐𝒓𝒓𝒆𝒄𝒕𝒂𝒎𝒆𝒏𝒕𝒆\n\n `{k}` ➥ `{t}`")
			shutil.move(actual,new)
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			return
		except Exception as ex:
			await bot.send_message(username,ex)
			return

@bot.on_message(filters.command("rename", prefixes="/") & filters.private)
async def rename(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	h = root[username]["actual_root"]
	lista = message.text.split(" ")
	name1 = int(lista[1])
	name2 = lista[2]
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	actual = str(root[username]["actual_root"]+"/")+msgh[1][name1]
	shutil.move(actual,h+"/"+name2)
	await send(f"𝑹𝒆𝒏𝒐𝒎𝒃𝒓𝒂𝒅𝒐 𝒄𝒐𝒓𝒓𝒆𝒄𝒕𝒂𝒎𝒆𝒏𝒕𝒆\n\n `{msgh[1][name1]}` ➥ `{name2}`")
	msg = files_formatter(str(root[username]["actual_root"]),username)
	await limite_msg(msg[0],username)
	return

@bot.on_message(filters.command("cd", prefixes="/")& filters.private)
async def cd(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	lista = msg.split(" ")
	j = str(root[username]["actual_root"])+"/"
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	if ".." in lista:
		lista = msg.split(" ")[1]
	else:
		lista = int(msg.split(" ")[1])
	path = str(j)
	if lista != "..":
		if not "." in msgh[1][lista]:
			cd = path + msgh[1][lista]
			root[username]["actual_root"] = str(cd)
			msg = files_formatter(cd,username)
			await limite_msg(msg[0],username)
			return
		else:
			await send("𝑺𝒐𝒍𝒐 𝒑𝒖𝒆𝒅𝒆 𝒎𝒐𝒗𝒆𝒓𝒔𝒆 𝒂 𝒖𝒏𝒂 𝒄𝒂𝒓𝒑𝒆𝒕𝒂")
			return
	else:
		a = str(root[username]["actual_root"])
		b = a.split("/")[:-1]
		if len(b) == 1:
			await send("𝒀𝒂 𝒆𝒔𝒕𝒂 𝒆𝒏 𝒆𝒍 𝒅𝒊𝒓𝒆𝒄𝒕𝒐𝒓𝒊𝒐 𝒓𝒂𝒊𝒛")
			return
		else:
			a = str(root[username]["actual_root"])
			b = a.split("/")[:-1]	
			c = ""
			for i in b:
				c += i + "/"
			c = c.rstrip(c[-1])
			root[username]["actual_root"] = c
			msg = files_formatter(c,username)
			await limite_msg(msg[0],username)
			return

@bot.on_message(filters.command("ls", prefixes="/")& filters.private)
async def ls(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	msg = files_formatter(str(root[username]["actual_root"])+"/",username)
	await limite_msg(msg[0],username)
	return
    
@bot.on_message(filters.command("up", prefixes="/") & filters.private)
async def up(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	user_id = message.from_user.id
	print(11)
	print(12)
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	print(13)
	if username not in boss and Configs["s"] == "Off":
		await client.send_message(username,'⛔𝑬𝒔𝒕𝒂 𝒇𝒖𝒏𝒄𝒊𝒐𝒏 𝒆𝒔𝒕𝒂 𝒂𝒑𝒂𝒈𝒂𝒅𝒂')
		return
	else: pass	
	print(14)
	comp = comprobar_solo_un_proceso(username) 
	if comp != False:
		await send(comp)
		return
	print(15)
	total_proc = total_de_procesos()
	if total_proc != False:
		await send(total_proc)
		return
	print(16)
	list = int(message.text.split(" ")[1])		
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	print(17)
	try:
		path = str(root[username]["actual_root"]+"/")+msgh[1][list]
		print(18)
		msg = await send(f"𝑺𝒆𝒍𝒆𝒄𝒄𝒊𝒐𝒏𝒂𝒅𝒐 **{path}**")
		print(19)
		if Configs[username]["m"] == "u":
			fd = await uploadfile(path, user_id, msg, username)
		elif Configs[username]["m"] == "revistas":
			print('revistas')
			await up_revistas_api(path, msg, username)
		else:
			await uploaddraft(path, user_id, msg, username)
	except Exception as ex:
		await send(ex)

@bot.on_message(filters.regex("sub") & filters.private)
async def sub(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	user_id = message.from_user.id
	print(11)
	print(12)
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	print(13)
	if username not in boss and Configs["s"] == "Off":
		await client.send_message(username,'⛔𝑬𝒔𝒕𝒂 𝒇𝒖𝒏𝒄𝒊𝒐𝒏 𝒆𝒔𝒕𝒂 𝒂𝒑𝒂𝒈𝒂𝒅𝒂⛔')
		return
	else: pass	
	print(14)
	comp = comprobar_solo_un_proceso(username) 
	if comp != False:
		await send(comp)
		return
	print(15)
	total_proc = total_de_procesos()
	if total_proc != False:
		await send(total_proc)
		return
	print(16)
	if "_" in message.text:
		list = int(message.text.split("_")[1])
	else:
		list = int(message.text.split(" ")[1])
		msgh = files_formatter(str(root[username]["actual_root"]),username)
	print(17)
	try:
		path = str(root[username]["actual_root"]+"/")+msgh[1][list]
		print(18)
		msg = await send(f"𝑺𝒆𝒍𝒆𝒄𝒄𝒊𝒐𝒏𝒂𝒅𝒐 **{path}**")
		print(19)
		if Configs[username]["m"] == "u":
			fd = await uploadfile(path,user_id,msg,username)
		elif Configs[username]["m"] == "revistas":
			await up_revistas_api(path, msg, username)
		else:
			await uploaddraft(path,user_id,msg,username)
	except Exception as ex:
		await send(ex)

@bot.on_message(filters.command("tg", prefixes="/") & filters.private)
async def tg(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	comp = comprobar_solo_un_proceso(username) 
	if comp != False:
		await send(comp)
		return
	total_proc = total_de_procesos()
	if total_proc != False:
		await send(total_proc)
		return
	list = int(message.text.split(" ")[1])
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	try:
		path = str(root[username]["actual_root"]+"/")+msgh[1][list]
		msg = await send(f"𝑺𝒆𝒍𝒆𝒄𝒄𝒊𝒐𝒏𝒂𝒅𝒐 **{path}**")
		filename = msgh[1][list]
		start = time()
		r = await bot.send_document(username,path,file_name=filename,progress=downloadmessage_tg,
									progress_args=(filename,start,msg))	
		await msg.edit("𝑺𝒖𝒃𝒊𝒅𝒂 𝑪𝒐𝒎𝒑𝒍𝒆𝒕𝒂𝒅𝒂")
		return
	except Exception as ex:
		await send(ex)
		return

#procesos
@bot.on_message(filters.command("view_process", prefixes="/") & filters.private)
async def view_process(client: Client, message: Message):	
	global procesos
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	await send(f"𝑬𝒍 𝒃𝒐𝒕 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒕𝒊𝒗𝒐(𝒔) {str(procesos)} 𝒅𝒆 500 ")
	return

@bot.on_message(filters.command("cancel", prefixes="/") & filters.private)
async def cancel(client: Client, message: Message):	
	global procesos
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if id_de_ms[username]["proc"] == "Up":
		p = await client.send_message(username,"𝑷𝒓𝒐𝒄𝒆𝒔𝒂𝒏𝒅𝒐")
		try:
			await id_de_ms[username]["msg"].delete()
			id_de_ms[username] = {"msg":"", "proc":""}
			await p.edit("✅ 𝑷𝒓𝒐𝒄𝒆𝒔𝒐 𝑪𝒂𝒏𝒄𝒆𝒍𝒂𝒅𝒐")
			if procesos > 0:
					procesos -= 1
			return
		except:
				if procesos > 0:
					procesos -= 1
				id_de_ms[username] = {"msg":"", "proc":""}
				await p.edit("✅ 𝑷𝒓𝒐𝒄𝒆𝒔𝒐 𝑪𝒂𝒏𝒄𝒆𝒍𝒂𝒅𝒐")
				return
	else:
		await client.send_message(username,"𝑵𝒐 𝒉𝒂𝒚 𝒑𝒓𝒐𝒄𝒆𝒔𝒐𝒔 𝒅𝒆 𝒔𝒖𝒃𝒊𝒅𝒂 𝒒𝒖𝒆 𝒄𝒂𝒏𝒄𝒆𝒍𝒂𝒓")
		return

#comandos de admin
@bot.on_message(filters.command("supr_process", prefixes="/") & filters.private)
async def supr_process(client: Client, message: Message):	
	global procesos
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		procesos = 0
		await send(f"✅ Operacion Realizada ✅")
	else:return

@bot.on_message(filters.command("change_status", prefixes="/") & filters.private)
async def change_status(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		if Configs["s"] == "Off":
			Configs["s"] = "On"
		else:
			Configs["s"] = "Off"
		await send(f"__**Status cambiado a **__"+  Configs["s"])
	
	else :
		await send("🚷 𝑪𝒐𝒎𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒂𝒅𝒎𝒊𝒏𝒊𝒔𝒕𝒓𝒂𝒅𝒐𝒓𝒆𝒔")
		return

@bot.on_message(filters.command("users", prefixes="/") & filters.private)
async def users(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:	
		total = len(Configs) - 10
		message = "**Usuarios: **"+ str(total)+'\n\n'
		for user in Configs:
			if user == "uclv":continue
			if user == "gtm":continue
			if user == "uvs":continue
			if user == "ltu":continue
			if user == "vcl":continue
			if user == "uccfd":continue
			if user == "ucuser":continue
			if user == "ucpass":continue
			if user == "gp":continue
			if user == "s":continue
			if user == "UHTRED_OF_BEBBANBURG":continue
			if user == "avatar23":continue
			if user == "Locura05":continue
			if user == "mcfee2828":continue
			if user == "uclv_p":continue
			message+=f"{user}\n"
		msg = f"{message}\n"
		await client.send_message(username,msg)
	else :
		await send("🚷 𝑪𝒐𝒎𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒂𝒅𝒎𝒊𝒏𝒊𝒔𝒕𝒓𝒂𝒅𝒐𝒓𝒆𝒔")
		return


@bot.on_message(filters.command("add", prefixes="/") & filters.private)
async def add(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:
		list = message.text.split(" ")						
		uss = list[1]
		Configs[uss] = {"z":99,"m":"u","a":"c","t":"y","gp":False,"host":"","user":"","passw":"","up_id":"","mode":""}
		total_up[uss] = {'P':0,'S':0}
		rvs[uss] = {'h':'','u':'','p':'','up':'','z':0}
	
		await client.send_message(username,f"@{uss} 🔥Le has otorgado acceso al bot🔥")
		await bot.send_message(uss, "❗️❗️Tienes Acceso Mamawebo❗️❗️")
	else :
		await send("🚷 𝑪𝒐𝒎𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒂𝒅𝒎𝒊𝒏𝒊𝒔𝒕𝒓𝒂𝒅𝒐𝒓𝒆𝒔 🚷")
		return


@bot.on_message(filters.command("rv", prefixes="/") & filters.private)
async def rv(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	else:
		list = message.text.split(" ")
		if len(list) != 6:
			ms = '❌ Error en el comando\nForma correcta:\n/rv host user passw zip up_id'
			await send(ms)
			return
		else:
			host = list[1]
			user = list[2]
			passw = list[3]
			zips = list[4]
			up_id = list[5]
   
			Configs[username]['m'] = 'revistas'
   
			Configs[username]['host'] = host
			Configs[username]['user'] = user
			Configs[username]['passw'] = passw
			Configs[username]['z'] = int(zips)
			Configs[username]['up_id'] = up_id

			ms = f'✴️ Revistas Config:\n\n⚜️ Host: {host}\n⚜️ Username: {user}\n⚜️ Password: {passw}\n⚜️ Up ID: {up_id}\n⚜️ Zips: {zips} mb'
			await send(ms)


@bot.on_message(filters.command("traffic", prefixes="/") & filters.private)
async def traffic(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	else:
		P = sizeof_fmt(total_up[username]['P'])
		S = sizeof_fmt(total_up[username]['S'])
		msg = f'📯 Tráfico Total 📯\n\n♛ Procesado: {P}\n♛ Subido: {S}'
		await send(msg)
		return


@bot.on_message(filters.command("kick", prefixes="/") & filters.private)
async def kick(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if username in boss:			
		list = message.text.split(" ")
		uss = list[1]
		del Configs[uss]
	
		await client.send_message(username,f'@{uss}**Ya no tiene acceso**')
	else :
		await send("🚷 𝑪𝒐𝒎𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒂𝒅𝒎𝒊𝒏𝒊𝒔𝒕𝒓𝒂𝒅𝒐𝒓𝒆𝒔")
		return

#descarga de archivos y enlaces
@bot.on_message(filters.media & filters.private)
async def delete_draft_y_down_media(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	else:
		downlist[username].append(message)
		await send("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝑪𝒂𝒓𝒈𝒂𝒅𝒐, 𝒖𝒔𝒆 __/download__ 𝒔𝒊 𝒆𝒔 𝒆𝒍 𝒖𝒍𝒕𝒊𝒎𝒐", quote=True)
		print(len(downlist[username]))
		return

@bot.on_message((filters.regex("https://") | filters.regex("http://")) & filters.private)
async def down_link(client: Client, message: Message):
	print(message)
	global procesos
	try:username = message.from_user.username
	except:
		print("Username no valido")
		return
	send = message.reply
	user_id = message.from_user.id
	if comprobacion_de_user(username) == False:
		intento_msg = "@" + username + " 🔥Intento usarme sin su permiso🔥"
		await send("❗️ No puede usarme contacte a mi Propietario.❗️👇\n https://t.me/zorritotheboss\n De momento voy a decirle q usted intento usarme sin su permiso\n")
		await bot.send_message(chat_id='6951967340', text=intento_msg)
		return
	if "youtu.be/" in message.text or "twitch.tv/" in message.text or "youtube.com/" in message.text or "xvideos.com" in message.text or "xnxx.com" in message.text:
		list = message.text.split(" ")
		initial_count = 0
		dir = 'downloads/'+ str(username)+'/'
		for path in os.listdir(dir):
			if os.path.isfile(os.path.join(dir, path)):
				initial_count += 1
		if initial_count == 0:
			pass
		else:
			await client.send_message(username,'🙂Su almacenamiento esta ocupado, para continuar use **/deleteall**')
			return
		url = list[0]
		try:format = str(list[1])
		except:format = "720"
		msg = await send("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
		await client.send_message(boss,f'**@{username} Envio un link de #youtube:**\n**Url:** {url}\n**Formato:** {str(format)}p')
		procesos += 1
		download = await ytdlp_downloader(url,user_id,msg,username,lambda data: download_progres(data,msg,format),format)
		if procesos != 0:
			procesos -= 1
		await msg.edit("𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂 𝒆𝒙𝒊𝒕𝒐𝒔𝒂")
		await msg.edit("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝒈𝒖𝒂𝒓𝒅𝒂𝒅𝒐")
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		return
	
	elif "https://www.mediafire.com/" in message.text:
		initial_count = 0
		dir = 'downloads/'+ str(username)+'/'
		for path in os.listdir(dir):
			if os.path.isfile(os.path.join(dir, path)):
				initial_count += 1
		if initial_count == 0:
			pass
		else:
			await client.send_message(username,'🙂Su almacenamiento esta ocupado, para continuar use **/deleteall**')
			return
		url = message.text
		if "?dkey=" in str(url):
			url = str(url).split("?dkey=")[0]
		msg = await send("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
		await client.send_message(boss,f'**@{username} Envio un link de #mediafire:**\n**Url:** {url}\n')
		procesos += 1
		file = await download_mediafire(url, str(root[username]["actual_root"])+"/", msg, callback=mediafiredownload)
		if procesos != 0:
			procesos -= 1
		await msg.edit("𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂 𝒆𝒙𝒊𝒕𝒐𝒔𝒂")
		await msg.edit("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝒈𝒖𝒂𝒓𝒅𝒂𝒅𝒐")
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		return
          
	elif "https://mega.nz/file/" in message.text:
		initial_count = 0
		dir = 'downloads/'+ str(username)+'/'
		for path in os.listdir(dir):
			if os.path.isfile(os.path.join(dir, path)):
				initial_count += 1
		if initial_count == 0:
			pass
		else:
			await client.send_message(username,'🙂Su almacenamiento esta ocupado, para continuar use **/deleteall**')
			return
		url = message.text
		mega = pymegatools.Megatools()
		try:
			filename = mega.filename(url)
			g = await send(f"Descargando su Archivo espere {filename} ...")
			data = mega.download(url,progress=None)	
			procesos += 1
			shutil.move(filename,str(root[username]["actual_root"]))
			await g.delete()
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			if procesos != 0:
				procesos -= 1
			return
		except Exception as ex:
			if procesos != 0:
				procesos -= 1
			if "[Error al descargar de Mega]" in str(ex): pass
			else:
				await send(ex)	
				return
	else:
		j = str(root[username]["actual_root"])+"/"

		url = message.text
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as r:
				try:
					filename = unquote_plus(url.split("/")[-1])
				except:
					filename = r.content_disposition.filename	
				fsize = int(r.headers.get("Content-Length"))
				total_up[username]['P']+=fsize
				msg = await send("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
				procesos += 1
				await client.send_message(boss,f'**@{username} Envio un #link :**\n**Url:** {url}\n')
				f = open(f"{j}{filename}","wb")
				newchunk = 0
				start = time()
				async for chunk in r.content.iter_chunked(1024*1024):
					newchunk+=len(chunk)
					await mediafiredownload(newchunk,fsize,filename,start,msg)
					f.write(chunk)
				f.close()
				file = f"{j}{filename}"
				await msg.edit("𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂 𝒆𝒙𝒊𝒕𝒐𝒔𝒂")
				if procesos != 0:
					procesos -= 1
				await msg.edit("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝒈𝒖𝒂𝒓𝒅𝒂𝒅𝒐")
				msg = files_formatter(str(root[username]["actual_root"]),username)
				await limite_msg(msg[0],username)
				return
      
#funciones
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)

def get_webservice_token(host='',username='',password='',proxy=None): 
	try:
		pproxy = None 
		webserviceurl = f'{host}login/token.php?service=moodle_mobile_app&username={username}&password={password}' 
		resp = requests.get(webserviceurl, proxies=pproxy,timeout=8) 
		data = json.loads(resp.text) 
		if data['token']!='': 
			return data['token'] 
		return None 
	except: return None



def descomprimir(archivo,ruta):
	archivozip = archivo
	with ZipFile(file = archivozip, mode = "r", allowZip64 = True) as file:
		archivo = file.open(name = file.namelist()[0], mode = "r")
		archivo.close()
		guardar = ruta
		file.extractall(path = guardar)

async def limite_msg(text,username):
	lim_ch = 1500
	text = text.splitlines() 
	msg = ''
	msg_ult = '' 
	c = 0
	for l in text:
		if len(msg +"\n" + l) > lim_ch:		
			msg_ult = msg
			await bot.send_message(username,msg)	
			msg = ''
		if msg == '':	
			msg+= l
		else:		
			msg+= "\n" +l	
		c += 1
		if len(text) == c and msg_ult != msg:
			await bot.send_message(username,msg)

def update_progress_bar(inte,max):
	percentage = inte / max
	percentage *= 100
	percentage = round(percentage)
	hashes = int(percentage / 5)
	spaces = 20 - hashes
	progress_bar = "[ " + " ■" * hashes + " " * spaces + " ] " + str(percentage) + "%"
	percentage_pos = int(hashes / 1)
	percentage_string = str(percentage) + "%"
	progress_bar = progress_bar[:percentage_pos] + progress_bar[percentage_pos :]
	return(progress_bar)

def iprox(proxy):
    tr = str.maketrans(
        "@./=#$%&:,;_-|0123456789abcd3fghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBAzyIwvutsrqponmlkjihgf3dcba9876543210|-_;,:&%$#=/.@",
    )
    return str.translate(proxy[::2], tr) 

def files_formatter(path, username):
	rut = str(path)
	filespath = Path(str(path))
	result = []
	dirc = []
	final = []
	for p in filespath.glob("*"):
		if p.is_file():
			result.append(str(Path(p).name))
		elif p.is_dir():
			dirc.append(str(Path(p).name))
	result.sort()
	dirc.sort()
	msg = f'𝑫𝒊𝒓𝒆𝒄𝒕𝒐𝒓𝒊𝒐 𝒂𝒄𝒕𝒖𝒂𝒍\n\n `{str(rut).split("downloads/")[-1]}`\n\n'
	if result == [] and dirc == [] :
		return msg , final
	for k in dirc:
		final.append(k)
	for l in result:
		final.append(l)
	i = 0
	for n in final:
		try:
			size = Path(str(path)+"/"+n).stat().st_size
		except: pass
		if not "." in n:
			msg+=f"╭➣❮ /seven_{i} ❯─❮ /rmdir_{i} ❯\n╰➣📂Carpeta: `{n}`\n\n"
		else:
			msg+=f"╭➣❮ /up_{i} ❯─❮ /rm_{i} ❯\n╰➣ {sizeof_fmt(size)} - `📃 {n}`\n"
		i+=1
	msg+= f"\n𝑬𝒍𝒊𝒎𝒊𝒏𝒂𝒓 𝒅𝒊𝒓𝒆𝒄𝒕𝒐𝒓𝒊𝒐 𝒓𝒂𝒊𝒛\n**/deleteall**"
	return msg , final

async def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]

async def download_mediafire(url, path, msg, callback=None):
	session = aiohttp.ClientSession()
	response = await session.get(url)
	url = await extractDownloadLink(await response.text())
	response = await session.get(url)
	filename = response.content_disposition.filename
	f = open(path+"/"+filename, "wb")
	chunk_ = 0
	total = int(response.headers.get("Content-Length"))
	start = time()
	while True:
		chunk = await response.content.read(1024)
		if not chunk:
			break
		chunk_+=len(chunk)
		if callback:
			await callback(chunk_,total,filename,start,msg)
		f.write(chunk)
		f.flush()
	return path+"/"+filename

def sevenzip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+".7z"), mode="wb", volume=volume, ext_digits=ext_digits
    ) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

def filezip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+"zip"), mode="wb", volume=volume, ext_digits=0) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

def update(username):
    Configs[username] = {"z": 900,"m":"e","a":"a"}
# async def get_messages():
# 	msg = await bot.get_messages(boss, message_ids=db_access)
# 	Configs.update(loads(msg.text))
# 	return
# async def send_config():
# 	try:
# 		await bot.edit_message_text(boss,message_id=db_access,text=dumps(Configs,indent=4))
# 	except:
# 		await bot.send_message(boss,text=dumps(Configs,indent=4))
# 		pass

async def ytdlp_downloader(url,usid,msg,username,callback,format):
	class YT_DLP_LOGGER(object):
		def debug(self,msg):
			pass
		def warning(self,msg):
			pass
		def error(self,msg):
			pass
	j = str(root[username]["actual_root"])+"/"
	resolution = str(format)	
	dlp = {"logger":YT_DLP_LOGGER(),"progress_hooks":[callback],"outtmpl":f"./{j}%(title)s.%(ext)s","format":f"best[height<={resolution}]"}
	downloader = yt_dlp.YoutubeDL(dlp)
	loop = asyncio.get_running_loop()
	filedata = await loop.run_in_executor(None,downloader.extract_info, url)
	filepath = downloader.prepare_filename(filedata)
	return filedata["requested_downloads"][0]["_filename"]	

seg = 0
def download_progres(data,message,format):
	if data["status"] == "downloading":
		filename = data["filename"].split("/")[-1]
		_downloaded_bytes_str = data["_downloaded_bytes_str"]
		_total_bytes_str = data["_total_bytes_str"]
		if _total_bytes_str == "N/A":
			_total_bytes_str = data["_total_bytes_estimate_str"]		
		_speed_str = data["_speed_str"].replace(" ","")
		_format_str = format		
		msg = f"📦 Nombre: {filename}\n\n"
		msg+= f"▶️ Descargando: {_downloaded_bytes_str}\n\n 🗂 Total: {_total_bytes_str}\n\n"
		msg+= f"🎥Resolución: {_format_str}p\n\n"	
		global seg 
		if seg != localtime().tm_sec:
			try:message.edit(msg,reply_markup=message.reply_markup)
			except:pass
		seg = localtime().tm_sec
async def downloadmessage_progres(chunk,filesize,filename,start,message):
		now = time()
		diff = now - start
		mbs = chunk / diff
		msg = f"📦 Nombre: {filename}\n\n"
		try:
			msg += update_progress_bar(chunk, filesize) + "\n\n ⚡️ Velocidad: " + sizeof_fmt(mbs) + "/s\n\n"
		except:pass
		msg+= f"▶️ Descargando: {sizeof_fmt(chunk)}\n\n 🗂 Total: {sizeof_fmt(filesize)}\n\n"	
		global seg
		if seg != localtime().tm_sec:
			try: await message.edit(msg)
			except:pass
		seg = localtime().tm_sec
def uploadfile_progres(chunk,filesize,start,filename,message):
	now = time()
	diff = now - start
	mbs = chunk / diff
	msg = f"📦 Nombre: {filename}\n\n"
	try:
		msg += update_progress_bar(chunk, filesize) + "\n\n ⚡️ Velocidad: " + sizeof_fmt(mbs) + "/s\n\n"
	except:pass
	msg+= f"▶️ Subiendo: {sizeof_fmt(chunk)}\n\n 🗂 Total: {sizeof_fmt(filesize)}\n\n"
	global seg
	if seg != localtime().tm_sec:
		message.edit(msg)
	seg = localtime().tm_sec
async def mediafiredownload(chunk,total,filename,start,message):
	now = time()
	diff = now - start
	mbs = chunk / diff
	msg = f"📦 Nombre: {filename}\n\n"
	try:
		msg += update_progress_bar(chunk, chunk) + "\n\n ⚡️Velocidad: " + sizeof_fmt(mbs) + "/s\n\n"
	except: pass
	msg+= f"▶️ Descargando: {sizeof_fmt(chunk)} 🗂 Total: {sizeof_fmt(total)}\n\n"
	global seg
	if seg != localtime().tm_sec:
		try: await message.edit(msg)
		except:pass
	seg = localtime().tm_sec
async def downloadmessage_tg(chunk,filesize,filename,start,message):
		now = time()
		diff = now - start
		mbs = chunk / diff
		msg = f"📦 Nombre: {filename}\n\n"
		try:
			msg += update_progress_bar(chunk, filesize) + "\n\n ⚡️ Velocidad: " + sizeof_fmt(mbs) + "/s\n\n"
		except:pass    
		msg+= f"▶️ Subido:: {sizeof_fmt(chunk)} 🗂 Total: {sizeof_fmt(filesize)}\n\n"	
		global seg
		if seg != localtime().tm_sec:
			try: await message.edit(msg)
			except:pass
		seg = localtime().tm_sec


class MoodleClient:
	def __init__(self,username,password,moodle,proxy):
		self.url = moodle
		self.username = username
		self.password = password
		self.session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True),connector=proxy)
		self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"}
		
	async def uploadtoken(self,f,progress,token):
		url = self.url+"/webservice/upload.php"
		file = Progress(f,progress)
		query = {"token":token,"file":file}
		async with self.session.post(url,data=query,headers=self.headers,ssl=False) as response:
			text = await response.text()
		dat = loads(text)[0]
		url = self.url+"/draftfile.php/"+str(dat["contextid"])+"/user/draft/"+str(dat["itemid"])+"/"+str(quote(dat["filename"]))
		urlw = self.url+"/webservice/rest/server.php?moodlewsrestformat=json"
		query = {"formdata":f"name=Event&eventtype=user&timestart[day]=31&timestart[month]=9&timestart[year]=3786&timestart[hour]=00&timestart[minute]=00&description[text]={quote_plus(url)}&description[format]=1&description[itemid]={randint(100000000,999999999)}&location=&duration=0&repeat=0&id=0&userid={dat['userid']}&visible=1&instance=1&_qf__core_calendar_local_event_forms_create=1","moodlewssettingfilter":"true","moodlewssettingfileurl":"true","wsfunction":"core_calendar_submit_create_update_form","wstoken":token}
		async with self.session.post(urlw,data=query,headers=self.headers,ssl=False) as response:
			text = await response.text()	
		try:
			a = findall("https?://[^\s\<\>]+[a-zA-z0-9]",loads(text)["event"]["description"])[-1].replace("pluginfile.php/","webservice/pluginfile.php/")+"?token="+token	
			return a , url	
		except:
			return url

		
class Progress(BufferedReader):
    def __init__(self, filename, read_callback):
        f = open(filename, "rb")
        self.filename = Path(filename).name
        self.__read_callback = read_callback
        super().__init__(raw=f)
        self.start = time()
        self.length = Path(filename).stat().st_size

    def read(self, size=None):
        calc_sz = size
        if not calc_sz:
            calc_sz = self.length - self.tell()
        self.__read_callback(self.tell(), self.length,self.start,self.filename)
        return super(Progress, self).read(size)
    
    
#Acceso de Uso al BoT
def comprobacion_de_user(username):
	if username in Configs or username in boss:			
		if exists('downloads/'+str(username)+'/'):pass
		else:os.makedirs('downloads/'+str(username)+'/')	
		try:Urls[username]
		except:Urls[username] = []
		try:Config[username]
		except:Config[username] = {"username":"","password":"","repoid":"","host":""}
		try:id_de_ms[username]
		except:id_de_ms[username] = {"msg":"","proc":""}
		try:root[username]
		except:root[username] = {"actual_root":f"downloads/{str(username)}"}
		try:downlist[username]
		except:downlist[username] = []
	else:
		return False

def comprobar_solo_un_proceso(username):
    if id_de_ms[username]["proc"] == "Up" :
        rup = "`Por Favor Espere, Ya posee una Tarea Activa\nUse: ` **/cancel** ` para Cancelar ❌ la Actual`"
        return rup
    else:
        return False

def total_de_procesos():
    global procesos
    hgy = "`⚠️BoT Ocupado, Prueba más Tarde ⚠️`"
    if procesos >= 100:
        return hgy
    else:
        return False


async def uploaddraft(file,usid,msg,username):
	user = Config[username]["username"]
	password = Config[username]["password"]
	host = Config[username]["host"]
	repoid = Config[username]["repoid"]
	zips = Configs[username]["z"]
	proxy = Configs[username]["gp"]
	print(1000)

	if proxy == False:
		connector = None
	else:
		connector = proxy
	if proxy == False:
		connection = aiohttp.TCPConnector()
	else:
		connection = aiohttp_socks.ProxyConnector(ssl=False).from_url(f"{proxy}")
	
	session = aiohttp.ClientSession(connector=connection)
	await msg.edit("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
	filename = Path(file).name
	filesize = Path(file).stat().st_size
	zipssize = 1024*1024*int(zips)
	
	await msg.edit("❗𝑪𝒐𝒎𝒑𝒓𝒐𝒃𝒂𝒏𝒅𝒐 𝒔𝒆𝒓𝒗𝒊𝒅𝒐𝒓")
	try:
		async with session.get(host,timeout=20,ssl=False) as resp:
			await resp.text()
			await msg.edit("𝑺𝒆𝒓𝒗𝒊𝒅𝒐𝒓 𝑶𝒏𝒍𝒊𝒏𝒆 ✔")
	except Exception as ex:
		await msg.edit(f"{host} is Down:\n\n{ex}")
		return
	
	id_de_ms[username] = {"msg":msg, "pat":filename, "proc":"Up"}
	
	if filesize > zipssize:
		await msg.edit("📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
		files = sevenzip(file,volume=zipssize)
		
		client = MoodleClient2(host,user,password,repoid,connector)
		links = []
		for file in files:	
			try:
				upload = await client.LoginUpload(file,lambda size,total,start,filename: uploadfile_progres(size,total,start,filename,msg))
				await bot.send_message(usid,f"**{upload}**")
				links.append(upload)
			except Exception as ex:
				if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
				else:
					await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓:\n\n{ex}")
				id_de_ms[username]["proc"] = ""
				return
		message = ""
		for link in links:
			message+=f"{link}\n"
		await msg.edit("✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆")
		with open(filename+".txt","w") as txt:
			txt.write(message)
		await bot.send_document(usid,filename+".txt",caption="Gracias por usar nuestros sevicios\nPara continuar subiendo use **/ls** :)")
		if username in boss:
			pass
		else:
			await bot.send_message(boss,f"✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆\n\n𝑵𝒐𝒎𝒃𝒓𝒆: {filename}\n🖇{message}")
			await bot.send_document(boss,filename+".txt")
		id_de_ms[username]["proc"] = ""
		os.unlink(filename+".txt")
		return
	else:
		client = MoodleClient2(host,user,password,repoid,connector)
		try:
			upload = await client.LoginUpload(file,lambda size,total,start,filename: uploadfile_progres(size,total,start,filename,msg))
			await msg.edit(f"__**{upload}**__")
			with open(filename+".txt","w") as txt:
				txt.write(upload)
			await bot.send_document(usid,filename+".txt",caption="Gracias por usar nuestros sevicios\nPara continuar subiendo use **/ls** :)")
			if username in boss:
				pass
			else:
				await bot.send_message(boss,f"✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆\n\n𝑵𝒐𝒎𝒃𝒓𝒆: {filename}\n🖇{upload}")
				await bot.send_document(boss,filename+".txt")
			id_de_ms[username]["proc"] = ""
			os.unlink(filename+".txt")
			return
		except Exception as ex:
			if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
			else:
				await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓:\n\n{ex}")
			id_de_ms[username]["proc"] = ""
			return

async def uploadfile(file,usid,msg,username):
	proxy = Configs["gp"]
	mode = Configs[username]["a"]
	usernamew = ''
	passwordw = ''
	
	if mode == "c":
		moodle = "https://moodle.uclv.edu.cu"
		token = Configs["uclv"]
		connector = aiohttp.TCPConnector()
	elif mode == "h":
		moodle = "https://aulauvs.gtm.sld.cu"
		token = Configs["gtm"]
		if proxy == "":
			connector = aiohttp.TCPConnector()
		else:
			connector = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
	elif mode == "b":
		moodle = "https://uvs.ucm.cmw.sld.cu"
		token = Configs["uvs"]
		if proxy == "":
			connector = aiohttp.TCPConnector()
		else:
			connector = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
	elif mode == "l":
		moodle = "https://uvs.ltu.sld.cu"
		token = Configs["ltu"]
		if proxy == "":
			connector = aiohttp.TCPConnector()
		else:
			connector = aiohttp_socks.ProxyConnector(ssl=False).from_url(f"{proxy}")
	elif mode == "v":
		moodle = "https://www.aula.vcl.sld.cu"
		token = Configs["vcl"]
		if proxy == "":
			connector = aiohttp.TCPConnector()
		else:
			connector = aiohttp_socks.ProxyConnector(ssl=False).from_url(f"{proxy}")
	elif mode == "u":
		moodle = "https://moodle.uccfd.cu"
		token = Configs["uccfd"]
		if proxy == "":
			connector = aiohttp.TCPConnector()
		else:
			connector = aiohttp_socks.ProxyConnector(ssl=False).from_url(f"{proxy}")
	elif mode == "a":
		moodle = "https://moodle.uclv.edu.cu"
		uset = Config[username]["username"]
		pasel = Config[username]["password"]
		hot = Config[username]["host"]
		connector = aiohttp.TCPConnector()
		await msg.edit(f"𝑶𝒃𝒕𝒆𝒏𝒊𝒆𝒏𝒅𝒐 𝑻𝒐𝒌𝒆𝒏")
		try:
			token = get_webservice_token(hot,uset,pasel)
			await msg.edit(f"✅ 𝑻𝒐𝒌𝒆𝒏 𝑶𝒃𝒕𝒆𝒏𝒊𝒅𝒐")
		except:
			id_de_ms[username]["proc"] = ""
			return		
	elif mode == "t":
		moodle = "https://moodle.uclv.edu.cu"
		hot = "https://moodle.uclv.edu.cu/"
		uset = Configs["ucuser"]
		pasel = Configs["ucpass"]
		connector = aiohttp.TCPConnector()
		token = Configs["uclv_p"]	
	
	zips = Configs[username]["z"]

	if mode == "a" or mode == "c" or mode == "t":
		if int(zips) > 399:
			await msg.edit("⛔𝑺𝒊 𝒖𝒔𝒂 𝑼𝑪𝑳𝑽 𝒍𝒐𝒔 𝒛𝒊𝒑𝒔 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆𝒏 𝒔𝒆𝒓 𝒎𝒂𝒚𝒐𝒓𝒆𝒔 𝒂 399 𝑴𝑩")
			return
	elif mode  == "b":
		if int(zips) > 499:
			await msg.edit("⛔𝑺𝒊 𝒖𝒔𝒂 𝑼𝒗𝒔.𝒖𝒄𝒎 𝒍𝒐𝒔 𝒛𝒊𝒑𝒔 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆𝒏 𝒔𝒆𝒓 𝒎𝒂𝒚𝒐𝒓𝒆𝒔 𝒂 499 𝑴𝑩")
			return
	elif mode == "l":
		if int(zips) > 249:
			await msg.edit("⛔𝑺𝒊 𝒖𝒔𝒂 𝑼𝒗𝒔.𝒍𝒕𝒖 𝒍𝒐𝒔 𝒛𝒊𝒑𝒔 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆𝒏 𝒔𝒆𝒓 𝒎𝒂𝒚𝒐𝒓𝒆𝒔 𝒂 249 𝑴𝑩")
			return
	elif mode == "h":
		if int(zips) > 7:
			await msg.edit("⛔𝑺𝒊 𝒖𝒔𝒂 𝑨𝒖𝒍𝒂.𝒈𝒕𝒎 𝒍𝒐𝒔 𝒛𝒊𝒑𝒔 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆𝒏 𝒔𝒆𝒓 𝒎𝒂𝒚𝒐𝒓𝒆𝒔 𝒂 7 𝑴𝑩")
			return
	elif mode == "v":
		if int(zips) > 299:
			await msg.edit("⛔𝑺𝒊 𝒖𝒔𝒂 Aula.vcl 𝒍𝒐𝒔 𝒛𝒊𝒑𝒔 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆𝒏 𝒔𝒆𝒓 𝒎𝒂𝒚𝒐𝒓𝒆𝒔 𝒂 300 𝑴𝑩")
			return
	elif mode == "u":
		if int(zips) > 5:
			await msg.edit("⛔𝑺𝒊 𝒖𝒔𝒂 uccfd 𝒍𝒐𝒔 𝒛𝒊𝒑𝒔 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆𝒏 𝒔𝒆𝒓 𝒎𝒂𝒚𝒐𝒓𝒆𝒔 𝒂 5 𝑴𝑩")
			return
	
	session = aiohttp.ClientSession(connector=connector)
	await msg.edit("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
	filename = Path(file).name
	filesize = Path(file).stat().st_size
	zipssize = 1024*1024*int(zips)
	logerrors = 0
	error_conv = 0
	logslinks = []

	try:
		async with session.get(moodle,timeout=20,ssl=False) as resp:
			await resp.text()
			await msg.edit("✔ 𝑺𝒆𝒓𝒗𝒊𝒅𝒐𝒓 𝑶𝒏𝒍𝒊𝒏𝒆 ✔")
	except Exception as ex:
		await msg.edit(f"{moodle} is Down:\n\n{ex}")
		return

	id_de_ms[username] = {"msg":msg, "pat":filename, "proc":"Up"}

	if filesize-1048>zipssize:
		parts = round(filesize / zipssize)
		await msg.edit(f"📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
		files = sevenzip(file,volume=zipssize)
		await msg.edit("❗𝑪𝒐𝒎𝒑𝒓𝒐𝒃𝒂𝒏𝒅𝒐 𝒔𝒆𝒓𝒗𝒊𝒅𝒐𝒓")
		
		client = MoodleClient(usernamew,passwordw,moodle,connector)
	
		for path in files:
				while logerrors < 5:
					error_conv = 0
					try:
						upload = await client.uploadtoken(path,lambda chunk,total,start,filen: uploadfile_progres(chunk,total,start,filen,msg),token)
						
						if mode == "l" or mode == "b":
							upload = upload[1]
							upload = upload.replace('draftfile.php/','webservice/draftfile.php/')
							upload = str(upload) + '?token=' + token
						elif mode == "a" or mode == "t":
							while error_conv < 10:
							
								await msg.edit("𝑷𝒓𝒆𝒑𝒂𝒓𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒄𝒐𝒏𝒗𝒆𝒓𝒕𝒊𝒓")
								await msg.edit("𝑪𝒐𝒏𝒗𝒊𝒓𝒕𝒊𝒆𝒏𝒅𝒐, 𝒔𝒆𝒂 𝒑𝒂𝒄𝒊𝒆𝒏𝒕𝒆...")
								upload = upload[1]
								upload = True
								if upload != False:	
									upload = upload.replace('pluginfile.php/','webservice/pluginfile.php/')
									upload = str(upload) + '?token=' + token
									
									error_conv = 0
									break
								else:
									await msg.edit("𝑬𝒓𝒓𝒐𝒓, 𝒓𝒆𝒊𝒏𝒕𝒆𝒏𝒕𝒂𝒏𝒅𝒐")
									error_conv +=1
									
									continue	
						else: 
							upload = upload[0]
						
						if upload == False:
							await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓.")
							id_de_ms[username]["proc"] = ""
							return
						
						await bot.send_message(usid,f"__**{upload}**__",disable_web_page_preview=True)
						logslinks.append(upload)
						logerrors = 0
					
						break
					except Exception as ex:
				
						logerrors += 1
						if logerrors > 4:
							if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
							else:
								await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓:\n\n{ex}")
							id_de_ms[username]["proc"] = ""
							return
						
		if len(logslinks) == len(files):
				await msg.edit("✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆")
				with open(filename+".txt","w") as f:
					message = ""
					for li in logslinks:
						message+=li+"\n"
					f.write(message)		
				await bot.send_document(usid,filename+".txt",caption="Gracias por usar nuestros sevicios\nPara continuar subiendo use **/ls** :)")
				if mode != "a":
					await bot.send_message(boss,f"✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆\n\n𝑵𝒐𝒎𝒃𝒓𝒆: {filename}\n🖇{message}")
					await bot.send_document(boss,filename+".txt")
				id_de_ms[username]["proc"] = ""
				os.unlink(filename+".txt")
				return
		else:
				await msg.edit("𝑯𝒂 𝒇𝒂𝒍𝒍𝒂𝒅𝒐 𝒍𝒂 𝒔𝒖𝒃𝒊𝒅𝒂")	
				id_de_ms[username]["proc"] = ""
				return	
	
	else:		
		client = MoodleClient(usernamew,passwordw,moodle,connector)
	
		while logerrors < 5:
					error_conv = 0
					try:
						upload = await client.uploadtoken(file,lambda chunk,total,start,filen: uploadfile_progres(chunk,total,start,filen,msg),token)
					
						if mode == "l" or mode == "b":
							upload = upload[1]
							upload = upload.replace('draftfile.php/','webservice/draftfile.php/')
							upload = str(upload) + '?token=' + token
							
						elif mode == "a" or mode == "t":
							while error_conv < 10:
								
								await msg.edit("𝑷𝒓𝒆𝒑𝒂𝒓𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒄𝒐𝒏𝒗𝒆𝒓𝒕𝒊𝒓")
								await msg.edit("𝑪𝒐𝒏𝒗𝒊𝒓𝒕𝒊𝒆𝒏𝒅𝒐, 𝒔𝒆𝒂 𝒑𝒂𝒄𝒊𝒆𝒏𝒕𝒆...")
								upload = upload[1]
								upload = True
							
								if upload != False:	
									upload = upload.replace('pluginfile.php/','webservice/pluginfile.php/')
									upload = str(upload) + '?token=' + token
									
									error_conv = 0
									break
								else:
									await msg.edit("𝑬𝒓𝒓𝒐𝒓, 𝒓𝒆𝒊𝒏𝒕𝒆𝒏𝒕𝒂𝒏𝒅𝒐")
									error_conv +=1
									
									continue	
						else:
							upload = upload[0]
						
						if upload == False:
							await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓.")
							id_de_ms[username]["proc"] = ""
							return
						
						await bot.send_message(usid,f"__**{upload}**__",disable_web_page_preview=True)
						logslinks.append(upload)
						logerrors = 0
			
						break
					except Exception as ex:
						
						logerrors += 1
						if logerrors > 4:
							if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
							else:
								await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓:\n\n{ex}")
							id_de_ms[username]["proc"] = ""
							return
		if len(logslinks) == 1:
				await msg.edit("✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆")
				with open(filename+".txt","w") as f:
					message = ""
					lin = ""
					for li in logslinks:
						message+=li+"\n"
						lin+=li+"\n"
					f.write(message)				
				await bot.send_document(usid,filename+".txt",caption="Gracias por usar nuestros sevicios\nPara continuar subiendo use **/ls** :)")
				if mode != "a":
					await bot.send_message(boss,f"✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆\n\n𝑵𝒐𝒎𝒃𝒓𝒆: {filename}\n🖇{lin}")
					await bot.send_document(boss,filename+".txt")
				id_de_ms[username]["proc"] = ""
				os.unlink(filename+".txt")
				return
		else:
				await msg.edit("𝑯𝒂 𝒇𝒂𝒍𝒍𝒂𝒅𝒐 𝒍𝒂 𝒔𝒖𝒃𝒊𝒅𝒂")
				id_de_ms[username]["proc"] = ""
				return

async def up_revistas_api(path, msg: Message, username):
	try:
		await msg.edit('Subiendo a Revista...')
     
		host = Configs[username]["host"]
		user = Configs[username]['user']
		passw = Configs[username]['passw']
		up_id = Configs[username]['up_id']
		zip_size = Configs[username]['z'] * 1024 * 1024
		file = Path(path)
		filesize = file.stat().st_size
		uploaded_links = []
  
		async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
			client = RevClient(host=host, 
                      		   username=user, 
                      		   password=passw, 
                      		   session=session)
			login = await client.login()
			if login:
				if filesize > zip_size:
					parts = round(filesize / zip_size)
					await msg.edit(f"Comprimiendo...\n\nTotal: {parts} partes\n")
					files = sevenzip(fpath=file, password=None, volume=zip_size)
					await msg.edit(f"**Subiendo...**")
					for file_part in files:
						file_part = Path(file_part)
						await msg.edit(f"**Subiendo...\n\nName:** `{file_part.name}`")
						upload = await client.upload(file_part, up_id)
						if upload:
							await msg.reply(f'{upload}')
							uploaded_links.append(upload)
						else:
							await msg.reply(f'**Error al subir:** `{file_part.name}`')
				else:
					await msg.edit(f"**Subiendo...\n\nName:** `{file.name}`")
					upload = await client.upload(file, up_id)
					if upload:
						await msg.reply(f'{upload}')
						uploaded_links.append(upload) 
					else:
						await msg.reply(f'**Error al subir:** `{file.name}`')
				await msg.edit(f"**Subida Completada...**")

				with open('uploaded_links.txt', 'w') as file:
					file.write('\n'.join(uploaded_links))
				file.close()

				await msg.reply_document(document='uploaded_links.txt', 
                             			 caption=f"`{file.name}\n\n{len(uploaded_links)} Files Uploaded`")
				os.remove('uploaded_links.txt')
			else: 
				await msg.edit('Error en el Login')

	except Exception as ex:
		print(ex)
		await msg.reply(f"**Error:** `{ex}`")
	
	

print("started")
bot.start()
print('Running...')
bot.loop.run_forever()
