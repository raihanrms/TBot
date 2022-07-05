import os
import re
import telegram
import telegram.ext
import logging
import sys

import pandas_datareader as web
import PySimpleGUI as sg

from logging import Filter
from urllib import response
from matplotlib import ticker

from requests import request
from tkinter.messagebox import CANCEL, QUESTION
from random import randint
from cgitb import handler

from turtle import update
from urllib.request import Request
from dotenv import load_dotenv
from sqlalchemy import true
from telegram import Bot, Location,Update
from telegram.ext import Updater, CommandHandler, CallbackContext, run_async
from telegram.utils.request import Request
from zmq import CONNECT_TIMEOUT
from datetime import datetime
from pyrogram import Client, filters
from telebot import types
from asyncio.subprocess import Process
from telegram import CallbackQuery

# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, MessageHandler
from telegram.ext import ConversationHandler, CallbackQueryHandler
from telegram.ext import ContextTypes

# from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

# import botStarttime from python telegram bot
from telegram.ext import botStarttime
