import mysql.connector
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

DB_ADDRESS  = "localhost"
DB_PORT     = 3306
DB_USERNAME = "root"
DB_PASSWORD = "159632478"

def format_field(x):
    
    return '"{}"'.format(x) if isinstance(x, str) else str(x)

def get_connection():
    connection = mysql.connector.connect(
        host=DB_ADDRESS, 
        port=DB_PORT, 
        user=DB_USERNAME, 
        password=DB_PASSWORD)
    
    return connection


class DBConnection:
    def __init__(self):
        self.con = get_connection()
        self.cursor = self.con.cursor()
        
    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def getIdByName(self, table_name, column_name, filter_column, name):
        el_id = self.query("SELECT {} FROM genshin_guide.{} WHERE {} = '{}'".format(column_name, table_name, filter_column, name))
        return el_id[0][0]
    
    
    def removeByName(self, table_name, id_col, name_col, name):
        obj_id = self.getIdByName(table_name, id_col, name_col, name)
        req = """ DELETE FROM genshin_guide.{} 
                  WHERE ({} = {})""".format(table_name, id_col, obj_id)
        self.query(req)
        self.con.commit()
        
    
    def createCharacterByNames(self, name, region, weap, element, material, book, loc, boss, wBoss, rare):
        
        region_id = self.getIdByName('regions', 'region_id', 'region_name', region)
        weap_id = self.getIdByName('weapon_type', 'wepon_type_id', 'weapon_type_name', weap)
        element_id = self.getIdByName('elements', 'element_id', 'element_name', element)
        material_id = self.getIdByName('materials', 'material_id', 'material_name', material)
        book_id = self.getIdByName('books', 'book_id', 'book_name', book)
        loc_id = self.getIdByName('local_specialities', 'local_speciality_id', 'local_speciality_name', loc)
        boss_id = self.getIdByName('boss_materials', 'boss_material_id', 'boss_material_name', boss)
        wBoss_id = self.getIdByName('world_boss_materials', 'world_boss_material_id', 'world_boss_material_name', wBoss)
        
        req = """INSERT INTO genshin_guide.characters (character_name, region_id, weapon_type_id, element_id, material_id, book_id, local_specialties_id, boss_material_id, world_boss_material_id, character_rare) 
        VALUES ('{}', {}, {}, {}, {}, {}, {}, {}, {}, {});""".format(name, region_id, weap_id, element_id, material_id, book_id, loc_id, boss_id, wBoss_id, rare)
        self.query(req)
        self.con.commit()
        
    def createWeapon(self, w_name, w_rare, w_type):
        w_type_id = self.getIdByName('weapon_type', 'wepon_type_id', 'weapon_type_name', w_type)
        req = """INSERT INTO genshin_guide.weapon (weapon_name, weapon_rare, weapon_type) 
        VALUES ('{}', {}, {});""".format(w_name, w_rare, w_type_id)
        self.query(req)
        self.con.commit()
        
    def combobox(self, column_name, table_name, description):
        return widgets.Combobox(
            placeholder='Выберите название...',
            options=[el[0] for el in self.query("SELECT DISTINCT {} FROM genshin_guide.{}".format(column_name, table_name))],
            description=description,
            ensure_option=True,
            disabled=False,
            continuos_update=True
        )
    
    
    def sortCombobox(self, query, description):
        return widgets.Combobox(
            placeholder='Выберите название...',
            options=[el[0] for el in self.query(query)],
            description=description,
            ensure_option=True,
            disabled=False
        )
    
    def multiple(self, column_name, table_name, description):
        return widgets.SelectMultiple(
            # placeholder='Выберите название...',
            options=[el[0] for el in self.query("SELECT DISTINCT {} FROM genshin_guide.{}".format(column_name, table_name))],
            description=description,
            ensure_option=True,
            disabled=False
        )
    
    def int_slider(self, table_name, column):
        vmin,vmax = self.query("SELECT MIN({}) as min_val, MAX({}) as max_val from genshin_guide.{}".format(column, column, table_name))[0]
        return widgets.IntSlider(value=vmin, min=vmin, max=vmax)
        
        