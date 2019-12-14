#!/usr/bin/env python
# coding: utf-8

from IPython.display import Image, display_jpeg
import sys
import os
import re
import numpy as np
import cv2


class create_image:
	def display_all(self):
		display_jpeg(Image("blended.jpg"))

	def situ(self,objs):
		if '室内' in objs:
			return 'indoor'
		elif '屋外' in objs:
			return 'outdoor'
		return 'unknown'

	def persons(self,objs):
		p = r'(.*)人'
		pc = re.compile(p)
		persons = {'num': '0'}
		persons['smile'] = self.smile(objs)
		persons['pose'] = self.standing(objs)
		persons['closeup'] = self.up(objs)
		persons['table'] = self.table(objs)
		for obj in objs:
			result = pc.match(obj)
			if result:
				if result.group(1).isdecimal():
					persons['num'] = result.group(1)
				else:
					persons['num'] = '5' # 不明なので決めうちにする
				return persons
		return persons

	def smile(self,objs):
		if 'スマイル' in objs:
			#print('スマイル')
			return 'smile'
		return ''

	def table(self,objs):
		#if 'テーブル' in objs:
		if '座ってる' in objs:
			#print('座ってる' + str(objs))
			return 'table'
		return ''

	def up(self,objs):
		if 'クローズアップ' in objs:
			return 'closeup'
		return ''

	def standing(self,objs):
		for obj in objs:
			if '座ってる' in obj:
				#print('座ってる' + str(objs))
				return 'sitting'
		return 'standing'

	def objects(self,objs):
		pets= ['犬','猫']
		#countables = ['食べ物','画面', '犬','猫']
		countables = ['食べ物','画面']
		middles = ['家', 'ビル', '木', '植物']
		backgrounds1 = ['海', '山', '空', '屋外', '室内']
		backgrounds2 = ['屋外', '室内']
		objects = {'countables':[], 'pets':[], 'middles':[], 'backgrounds':[]}
		for obj in objs:
			if  obj in countables:
				objects['countables'].append(obj)
			elif obj in pets:
				objects['pets'].append(obj)
			elif obj in middles:
				objects['middles'].append(obj)
			elif obj in backgrounds1:
				objects['backgrounds'].append(obj)
		for obj in objs:
			if obj in backgrounds2:
				if len(objects['backgrounds']) == 0:
					objects['backgrounds'].append(obj)
		for obj in objs:
			if obj == '食べ物' and len(objs) != 1:
				objects['countables'].remove('食べ物')
		return objects

	def create_text_list(self,text):
		return text.split('、')

	def analyze(self,text):
		images = {}
		objs = text.split('、')
		images['situation'] = self.situ(objs)
		images['persons'] = self.persons(objs)
		images['objects'] = self.objects(objs)
		return images

	def analyze_list(self,text_list):
		images = {}
		images['situation'] = self.situ(text_list)
		images['persons'] = self.persons(text_list)
		images['objects'] = self.objects(text_list)
		return images

	def merge(self,base, img, x, y):
		base[y:y+img.shape[0], x:x+img.shape[1]] = img
		return base

	def get_masked(self,foreground, background):
		# グレースケールに変換する。
		gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
		# 2値化する。
		_, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
		# 輪郭抽出する。
		contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		# 検出された輪郭内部を255で塗りつぶす。
		mask = np.zeros_like(binary)
		cv2.drawContours(mask, contours, -1, color=255, thickness=-1)
		h, w = foreground.shape[:2]  # 前景画像の大きさ
		x, y = 0, 0  # 背景画像の座標上で前景画像を貼り付ける位置
		roi = background[y : y + h, x : x + w, :]
		masked_img = np.where(np.expand_dims(mask == 255, -1), foreground, roi)
		return masked_img

	def draw_middles(self,objs, base):
		return draw_images(objs, base, 0, 0)

	def draw_images(self,objs, base, x, y):
		images = {}
		for obj in objs:
			images[obj] = cv2.imread(f"images/{obj}.png")
			file = f"images/{obj}.png"
			if not os.path.isfile(file):
				print(f"{obj} not found\n")
				return base
			images[obj] = cv2.resize(images[obj], (base.shape[1], base.shape[0]))
			#print(f"{images[obj].shape[1]}, {images[obj][0]}")
			#images[obj] = cv2.cvtColor(images[obj], cv2.COLOR_BGR2RGB)
			masked = self.get_masked(images[obj], base)
			base = self.merge(base, masked, x, y)
		return base

	def draw_backgrounds(self,objs):
		#backgrounds = ['海', '山', '空', '屋外', '室内']
		bg1 = ['海', '山', '空']
		name = ""
		default ="images/white.png"
		if len(objs) == 1:
			name = f"images/{objs[0]}.png"
			if not os.path.isfile(name):
				name = default
		elif len(objs) == 2:
			name = f"{objs[0]}{objs[1]}.png"
			if not os.path.isfile(name):
				name = f"{objs[1]}{objs[0]}.png"
				if not os.path.isfile(name):
					name = default
		elif len(objs) == 3:
			name = 'images/海山空.png'
			if not os.path.isfile(name):
				name = default
		else:
			name = default
		base = cv2.imread(name)
		return base

	def draw_persons(self,persons, base):
		#  num, smile, pose, closeup, table
		# 3_closeup_standing_smile_table_persons
		if int(persons['num']) == 0:
			return base;
		if int(persons['num']) > 5:
			persons['num'] = 5
		img_name = f"images/{persons['num']}_{persons['closeup']}_{persons['pose']}_{persons['smile']}_{persons['table']}_persons.png"
		print(f"opening {img_name}...")
		if not os.path.isfile(img_name):
			print(f"{img_name} not found\n")
			return base
		person_img = cv2.imread(img_name)
		person_img = cv2.resize(person_img, (base.shape[1], base.shape[0]))
		masked = self.get_masked(person_img, base)
		base = self.merge(base, masked, 0, 0)

		return base

	def obaka_merge(self,objs,file_path):
		images = {}
		base = self.draw_backgrounds(objs['objects']['backgrounds'])

		base = self.draw_images(objs['objects']['middles'], base, 0, 0)
		base = self.draw_images(objs['objects']['countables'], base, 0, 0)
		base = self.draw_persons(objs['persons'], base)
		base = self.draw_images(objs['objects']['pets'], base, 0,0)
		# blended = cv2.addWeighted(src1=base,alpha=0.7,src2=images[obj],beta=0.3,gamma=0)
		cv2.imwrite(file_path, base)

	def create(self,tag_list,file_path):
		# alt text のパース
		#images = self.analyze_list(tag_list)
		images = self.analyze_list(tag_list)
		#print(images)

		# merge 処理
		self.obaka_merge(images,file_path)


if __name__ == "__main__":
	args = sys.argv
	count = len(args)
	if (count != 2):
		print('usage: merge.py alt-text')
		print('continue with "house", though')
		args[1] = '家'
		#sys.exit(-1)

	file_path = "obaka_merge.png"

	crt_img = create_image()
	text_list = crt_img.create_text_list(args[1])
	crt_img.create(text_list,file_path)
