import os
import telegram
import pandas_datareader as web

from logging import Filter
from urllib import response
from matplotlib import ticker

from turtle import update
from urllib.request import Request
from dotenv import load_dotenv
from sqlalchemy import true
from telegram import Bot, Location,Update
from telegram.ext import Updater,CommandHandler,CallbackContext
from telegram.utils.request import Request
from zmq import CONNECT_TIMEOUT
from datetime import datetime
from pyrogram import Client, filters

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, MessageHandler
from telegram.ext import ConversationHandler, CallbackQueryHandler
from telegram.ext import ContextTypes

# from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes