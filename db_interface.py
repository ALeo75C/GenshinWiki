import pandas as pd
from ipywidgets import interact, widgets

def sortInfo():
    req = ''
    return req

def getCharacter(db, rare, element, weapon):
    req = """SELECT c.character_name, e.element_name,  w.weapon_type_name
        FROM genshin_guide.characters c
        JOIN genshin_guide.elements e ON e.element_id = c.element_id
        JOIN genshin_guide.weapon_type w ON w.wepon_type_id = c.weapon_type_id
        WHERE c.character_rare = {}
        """.format(rare[-1])
    if len(element) == 0 and len(weapon) == 0:
        display(pd.DataFrame(db.query(req), columns=['name', 'element', 'weapon']))
    elif len(element) > 0 and len(weapon) == 0:
        req += """AND e.element_name IN {element:}"""
        display(pd.DataFrame(db.query(req.format(rare=rare[-1], element=str(element)).replace(',)', ')')), columns=['name', 'element', 'weapon']))
    elif len(element) == 0 and len(weapon) > 0:
        req += """AND w.weapon_type_name IN {weapon:}"""
        display(pd.DataFrame(db.query(req.format(rare=rare[-1], weapon=str(weapon)).replace(',)', ')')), columns=['name', 'element', 'weapon']))
    else:
        req += """AND w.weapon_type_name IN {weapon:}
                  AND e.element_name IN {element:}"""
        display(pd.DataFrame(db.query(req.format(rare=rare[-1], element=str(element), weapon=str(weapon)).replace(',)', ')')), columns=['name', 'element', 'weapon']))
            
        
        
    
def character_by_rare_element_and_weapon_interface(db):
    #'db': widgets.fixed(db),
    title = widgets.HTML(value="<h1>Выбор персонажей</h1>")
    h2 = widgets.HTML(value="<p>Качество персонажа:</p>")
    text = widgets.HTML(value="<br><p><i><b>Ctrl</b> для выбора нескольких пунктов</i></p>")
    rar = widgets.RadioButtons(
            options=[
                '★★★★ 4',
                '★★★★★ 5'
            ],
            layout={'width': 'max-content'}
        )
        
    element_widget = db.multiple('element_name', 'elements', 'Элементы:')
    wapon_widget = db.multiple('weapon_type_name', 'weapon_type', 'Тип оружия:')
    
    ui = widgets.VBox([title, h2, rar, text, element_widget, wapon_widget])
    out = widgets.interactive_output(getCharacter, { 'db': widgets.fixed(db), 'rare': rar, 'element': element_widget, 'weapon': wapon_widget})
    display(ui, out)
    
def getWeapon(db, rare, w_type):
    req = """SELECT w.weapon_name, wt.weapon_type_name
        FROM genshin_guide.weapon w
        JOIN genshin_guide.weapon_type wt ON w.weapon_type = wt.wepon_type_id
        WHERE w.weapon_rare = {} """.format(rare[-1])
    if len(w_type) == 0:
        display(pd.DataFrame(db.query(req), columns=['name', 'type']))
        
    else:
        req += """AND wt.weapon_type_name IN {w_type:}"""
        display(pd.DataFrame(db.query(req.format(rare=rare[-1], w_type=str(w_type)).replace(',)', ')')), columns=['name', 'type']))
    
    
def weapon_interface(db):
    title = widgets.HTML(value="<h1>Выбор оружия</h1>")
    h2 = widgets.HTML(value="<p>Качество оружия:</p>")
    text = widgets.HTML(value="<br><p><i><b>Ctrl</b> для выбора нескольких пунктов</i></p>")
    rar = widgets.RadioButtons(
            options=[
                '★ 1',
                '★★ 2',
                '★★★ 3',
                '★★★★ 4',
                '★★★★★ 5'
            ],
            layout={'width': 'max-content'}
        )

    wapon_widget = db.multiple('weapon_type_name', 'weapon_type', 'Тип оружия:')

    ui = widgets.VBox([title, h2, rar, text, wapon_widget])
    out = widgets.interactive_output(getWeapon, { 'db': widgets.fixed(db), 'rare': rar, 'w_type': wapon_widget})
    display(ui, out)
    
def group(db, src):
    req = """
            SELECT COUNT(wt.weapon_type_name), wt.weapon_type_name 
            FROM genshin_guide.weapon w
            JOIN genshin_guide.weapon_type wt ON w.weapon_type = wt.wepon_type_id
            WHERE w.sourse = '{}' 
            GROUP BY wt.weapon_type_name;
          """
    display(pd.DataFrame(db.query(req.format(src).replace(',)', ')')), columns=['count', 'type']))
    
def weaponSources(db):
    title = widgets.HTML(value="<h1>Количество оружия из разных источников</h1>")
    h2 = widgets.HTML(value="<p>Источник:</p>")
    src = db.query("SELECT Distinct(sourse) FROM genshin_guide.weapon")
    rar = widgets.RadioButtons(
            options=[
               i[0] for i in src
            ],
            layout={'width': 'max-content'}
        )


    ui = widgets.VBox([title, h2, rar])
    out = widgets.interactive_output(group, { 'db': widgets.fixed(db), 'src': rar,})
    display(ui, out)
    
# def ch(db, src):
#     req = """
#             SELECT character_name 
#             FROM genshin_guide.characters
#             WHERE chararacter_name = '{}' 
#           """
#     display(pd.DataFrame(db.query(req.format(src).replace(',)', ')')), columns=['name', 'type']))
    
# def character_materials_interface(db):
#     title = widgets.HTML(value="<h1>***</h1>")
#     character_widget = db.multiple('character_name', 'characters', 'Персонажи:')
#     print(character_widget.value)
#     # rar = widgets.RadioButtons(
#     #         options=[
#     #            i[0] for i in src
#     #         ],
#     #         layout={'width': 'max-content'}
#     #     )
# # JOIN genshin_guide.local_specialities ls ON c.local_specialties_id = ls.local_speciality_id

#     ui = widgets.VBox([title, character_widget])
#     out = widgets.interactive_output(ch, { 'db': widgets.fixed(db), 'src': character_widget.value,})
#     display(ui, out)
    
    
    
    
def foo(db, name, rare, element, region, weapon, material, ls, book, boss, wBoss):
    db.createCharacterByNames(name.value, region.value, weapon.value, element.value,  material.value, book.value, ls.value, boss.value, wBoss.value, rare.value[-1])


def region_filtered_select(db, column_name, table_name, region_name=None):
    query = """
        SELECT {}
        FROM genshin_guide.{}
    """.format(column_name, table_name)
    if region_name is not None:
        query += """
            WHERE region_id = (SELECT rg.region_id 
                               FROM genshin_guide.regions rg
                               WHERE rg.region_name = '{}')
        """.format(region_name)
    return [el[0] for el in db.query(query)]


def book_regioned_select(db, column_name, table_name, region_name=None):
    if not region_name:
        query = "SELECT {} FROM genshin_guide.{}".format(column_name, table_name)
    else:
        query = """
            SELECT b.book_name
            FROM genshin_guide.books b
            JOIN genshin_guide.dungeons d ON d.dungeon_id = b.dungeon_id
            WHERE d.region_id = (SELECT rg.region_id FROM genshin_guide.regions rg WHERE rg.region_name = '{}')
        """.format(region_name)
    return [el[0] for el in db.query(query)]


def combobox_filter_callback(checkbox, combobox, region_widget, db, column_name, table_name, select_fn=region_filtered_select):
    def callback(*args, **kwargs):
        with combobox.hold_trait_notifications():
            if checkbox.value:
                combobox.options = select_fn(db, column_name, table_name, region_widget.value)
            else:
                combobox.options = select_fn(db, column_name, table_name)
    
    return callback
    
    
def add_character(db):
    title = widgets.HTML(value="<h1>Добавить нового персонажа</h1>")
    line = widgets.HTML(value="<br>")
    
    sub_button = widgets.Button(
        description='Создать',
        disabled=False,
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Создать персонажа',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )
    
    filter_checkbox = widgets.Checkbox(
        value=False,
        description='Фильтровать по региону',
        disabled=False,
        button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Включает сортировку книг, диковинок и материалов с боссов по их расположению в регионах',
    )
    
    
    name_widget = widgets.Text(value='',
                               placeholder='Имя персонажа',
                               description='Имя:',
                               disabled=False)
    rare_widget = widgets.RadioButtons(
            options=[
                '★★★★ 4',
                '★★★★★ 5'
            ],
            layout={'width': 'max-content'}
        )
    
    # rare_widget = db.int_slider('characters', 'character_rare')
    element_widget = db.combobox('element_name', 'elements', 'Элемент:')
    region_widget = db.combobox('region_name', 'regions', 'Регион:')
    weapon_widget = db.combobox('weapon_type_name', 'weapon_type', 'Оружие:')
    material_widget = db.combobox('material_name', 'materials', 'Материал:')
    

    #    ls_widget = db.sortCombobox('local_speciality_name', 'genshin_guide.local_specialities', 'region_id', region_widget.value, 'Диковинка:')
    #else:
    ls_widget = db.combobox('local_speciality_name', 'local_specialities', 'Диковинка:')
    book_widget = db.combobox('book_name', 'books', 'Книга:')
    boss_widget = db.combobox('boss_material_name', 'boss_materials', 'Материал для возвышения:')
    wBoss_widget = db.combobox('world_boss_material_name', 'world_boss_materials', 'Материал для улучшения способностей:')
    
    kwargs = {'db': db, 'checkbox': filter_checkbox, 'region_widget': region_widget}
    ls_callback = combobox_filter_callback(combobox=ls_widget, column_name='local_speciality_name', table_name='local_specialities', **kwargs)
    book_callback = combobox_filter_callback(combobox=book_widget, column_name='book_name', table_name='books', select_fn=book_regioned_select, **kwargs)
    boss_callback = combobox_filter_callback(combobox=boss_widget, column_name='boss_material_name', table_name='boss_materials',  **kwargs)
    
    def checkbox_callback(*args, **kwargs):
        ls_callback()
        book_callback()
        boss_callback()
               
    filter_checkbox.observe(checkbox_callback, names='value')  
    region_widget.observe(checkbox_callback, names='value')
    ui = widgets.VBox([title, name_widget, rare_widget, element_widget,
                       region_widget, weapon_widget, material_widget,  wBoss_widget, line, 
                       filter_checkbox, line, book_widget, ls_widget,
                       boss_widget, sub_button])
    # out = widgets.interactive_output(getCharacterByRareAndElement, { 'db': widgets.fixed(db), 'rare': rare_widget, 'element': element_widget})
    def button_callback(b):
        foo(db,name_widget, rare_widget, element_widget, region_widget, weapon_widget, material_widget, ls_widget, book_widget, boss_widget, wBoss_widget)
        
    sub_button.on_click(button_callback)
    display(ui)
    
def add_weapon(db):
    title = widgets.HTML(value="<h1>Добавить новое оружие</h1>")
    line = widgets.HTML(value="<br>")
    
    sub_button = widgets.Button(
        description='Создать',
        disabled=False,
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Создать персонажа',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )
    
    name_widget = widgets.Text(value='',
                               placeholder='Название оружия',
                               description='Название:',
                               disabled=False)
    rare_widget = widgets.RadioButtons(
            options=[
                '★ 1',
                '★★ 2',
                '★★★ 3',
                '★★★★ 4',
                '★★★★★ 5'
            ],
            layout={'width': 'max-content'}
        )
    type_widget = db.combobox('weapon_type_name', 'weapon_type', 'Тип:')
    # source_widget =  widgets.Combobox(
    #                     placeholder='Выберите источник оружия...',
    #                     options=[el[0] for el in db.query('SELECT Distinct(sourse) FROM genshin_guide.weapon')],
    #                     description='Источник',
    #                     ensure_option=True,
    #                     disabled=False
    #                  )
    

    ls_widget = db.combobox('local_speciality_name', 'local_specialities', 'Диковинка:')
    book_widget = db.combobox('book_name', 'books', 'Книга:')
    boss_widget = db.combobox('boss_material_name', 'boss_materials', 'Материал для возвышения:')
    wBoss_widget = db.combobox('world_boss_material_name', 'world_boss_materials', 'Материал для улучшения способностей:')
    
    ui = widgets.VBox([title, name_widget, rare_widget, type_widget, sub_button])
                   
    
    def button_callback(b):
        print('CLICK')
        db.createWeapon(name_widget.value, rare_widget.value[-1], type_widget.value)
        
    sub_button.on_click(button_callback)
    display(ui)
    
    
    
    
def remove_block(db):
    title = widgets.HTML(value="<h1>Удаление</h1>")
    line = widgets.HTML(value="<br>")
    
    charcter_block = removeM(db, 'Персонажи', 'Выберете имя персонажа, которого хотите удалить', 'characters', 'character_name', 'character_id', 'Персонажи:   ')
    weapon_block = removeM(db, 'Оружие', 'Выберете название оружия, которое хотите удалить', 'weapon', 'weapon_name', 'weapon_id', 'Оружие:')
    
    ui = widgets.VBox([title]+charcter_block+weapon_block)  
    display(ui)


def removeM(db, h, text, table_name, column_name, id_col_name, title):
    text = widgets.HTML(value="<h3>"+h+"</h3><p>"+text+"</p>")
    widget = db.combobox(column_name, table_name, title)
    
    sub_button = widgets.Button(
        description='Удалить',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Удалить',
        icon='fa-eraser' # (FontAwesome names without the `fa-` prefix)
    )
        
    def button_callback(b):
        db.removeByName(table_name, id_col_name, column_name, widget.value)
    
    sub_button.on_click(button_callback)
    
    ui = [text, widget, sub_button]
    return ui
