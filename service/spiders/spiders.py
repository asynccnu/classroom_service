# -*- coding: utf-8 -*-


# 七号楼所有的教室
ALLROOM7 = [
        u'7101',u'7102',u'7103',u'7104',u'7105',u'7106',u'7107',u'7108',u'7109',
        u'7201',u'7202',u'7203',u'7204',u'7205',u'7206',u'7207',u'7208',u'7209',u'7211',
        u'7301',u'7302',u'7303',u'7304',u'7305',u'7306',u'7307',u'7308',u'7309',u'7311',
        u'7401',u'7402',u'7403',u'7404',u'7405',u'7406',u'7407',u'7408',u'7409',u'7410',u'7411',
        u'7501',u'7503',u'7505'
        ]

# 八号楼所有的教室
ALLROOM8 = [
        u'8101',u'8102',u'8103',u'8104',u'8105',u'8106',u'8107',u'8108',u'8109',
        u'8110',u'8111',u'8112',u'8201',u'8202',u'8203',u'8204',u'8205',u'8206',
        u'8207',u'8208',u'8209',u'8210',u'8211',u'8212',u'8213',u'8214',u'8215',
        u'8216',u'8301',u'8302',u'8303',u'8304',u'8305',u'8306',u'8307',u'8308',
        u'8309',u'8310',u'8311',u'8312',u'8313',u'8314',u'8315',u'8316',u'8401',
        u'8402',u'8403',u'8404',u'8405',u'8406',u'8407',u'8408',u'8409',u'8410',
        u'8411',u'8412',u'8413',u'8414',u'8415',u'8416',u'8501',u'8502',u'8503',
        u'8504',u'8505',u'8506',u'8507',u'8508',u'8509',u'8510',u'8511',u'8512',
        u'8513',u'8514',u'8515',u'8516',u'8716',u'8717'
        ]


def update_sheets(all_sheets, connection, Week, init=False, start_sheet=0, start_row=0):
    """
    更新所有年级的课表

    all_sheets: 包含各年级课表的xls对象(每列依次为: 上课时间1, 上课时间2, 上课时间3, 上课地点1, 上课地点2, 上课地点3)
    connection: MongoDB的Connection对象
    Week:       MongoDB的Week类
    init:       是否先初始化课表
    start_sheet:选择从哪张表开始
    start_row:  选择从哪一列开始
    """
    for each_sheet in all_sheets[start_sheet:]:
        update_each(each_sheet, connection, Week, init, start_row)


def update_each(sheet, connection, Week, init, start_row):
    """
    根据当前年级的课表更新空闲教室表

    sheet:      xls中的一页表
    connection: MongoDB的Connection对象
    Week:       MongoDB的Week类
    """

    def init_week(week_no, bno):
        """
        初始化每周每天对应的字典, 初始状态所有教室都空闲

        week_no: 周数           int
        bno:     楼栋号(7 或 8) unicode
        """

        def init_weekdays(weekday_list, bno):
            """
            将每天对应的节次的空闲教室设定为全部教室

            weekday_list: Week实例中'mon'~'fri'的字典对象
            bno:          楼栋号(7 或 8)                  unicode
            """
            for sec in range(1, 15):
                if int(bno) == 7:
                    room_list = ALLROOM7
                else:
                    room_list = ALLROOM8
                weekday_list[u'%d' % sec] = room_list

        week = connection.Week.find_one({'weekNo': u'week%d'%week_no, 'bno': bno}) or connection.Week()
        week['weekNo'] = u'week%d'%week_no
        week['bno'] = bno
        for wd in [u'mon', u'tue', u'wed', u'thu', u'fri']:
            week[wd] = dict()
            init_weekdays(week[wd], bno)
        week.save()

    # 初始化上课教室
    if init:
        for week_no in range(1, 21):
            for bno in [u'7', u'8']:
                init_week(week_no, bno)

    # 添加所有上课的教室
    rows_counts = sheet.nrows
    for row_no in range(rows_counts)[start_row:]:
        print "working on row: %d" % row_no
        values = sheet.row_values(row_no)
        times = values[:3]     # 上课时间 1-3
        locs = values[3:]  # 上课地点 1-3

        for i in range(3):
            time = times[i]
            if not time:
                break
            loc = locs[i]
            if (not isinstance(loc, float)) or (int(loc//1000) not in [7, 8]):
                break
            loc = u'%d' % int(loc)
            bno = loc[0]

            # 上课的星期(汉字: 一、二...)
            weekday = time[time.index(u'\u671f')+1]
            # 上课的节次
            try:
                sec_li = list(int(i) for i in time[time.index(u'\u7b2c')+1:time.index(u'\u8282')].split('-'))
            except ValueError:
                continue
            secs = range(sec_li[0], sec_li[1]+1)
            # 上课的周次
            week_li = list(int(i) for i in time[time.index('{')+1:time.index(u'\u5468')].split('-'))
            # 单双周筛选
            if u'\u5355' in time:
                weeks = list(each for each in range(week_li[0], week_li[1]+1) if each%2!=0)
            elif u'\u53cc' in time:
                weeks = list(each for each in range(week_li[0], week_li[1]+1) if each%2==0)
            else:
                weeks = list(each for each in range(week_li[0], week_li[1]+1))

            for each_week in weeks:
                if each_week > 20:
                    # 超过20周的课不进行计算
                    break
                found_week = connection.Week.find_one({'weekNo': u'week%d'%each_week, 'bno': bno})
                ewd = get_week_en(weekday)
                if not ewd:
                    # 星期六和星期日的课程不进行计算
                    break
                sec_room_dict = found_week[ewd] # 节次与教室的字典
                for sec in secs:
                    try:
                        index = sec_room_dict[u'%d'%sec].index(loc)
                    except ValueError:
                        # 列表中已经不存在这个教室
                        print "{} in list weekno{} bno{} sec{}? {}".format(loc, each_week, bno, sec, loc in sec_room_dict[u'%d'%sec])
                        break
                    # 从空闲教室列表中删除该教室
                    found_week[ewd][u'%d'%sec] = found_week[ewd][u'%d'%sec][:index] + found_week[ewd][u'%d'%sec][index+1:]
                found_week.save()


def get_week_en(ch):
    """
    根据星期的汉字获取英文

    ch: '一' or '二' or '三' or '四' or '五'
    """
    if ch == u'\u4e00':
        return u'mon'
    elif ch == u'\u4e8c':
        return u'tue'
    elif ch == u'\u4e09':
        return u'wed'
    elif ch == u'\u56db':
        return u'thu'
    elif ch == u'\u4e94':
        return u'fri'

if __name__ == '__main__':
    import os, xlrd
    from mongokit import Connection, Document

    class Week(Document):
        __collection__ = 'weeks'
        __database__ = 'weekdb'
        structure = {
                'bno': unicode,
                'weekNo': unicode,
                'mon': dict,
                'tue': dict,
                'wed': dict,
                'thu': dict,
                'fri': dict
        }
        def __repr__(self):
            return '<Mongo Week bno:{} weekNo:{}>'.format(self['bno'], self['weekNo'])
    data = xlrd.open_workbook(os.getenv("TABLE_PATH"))
    all_sheets = data.sheets()
    connection = Connection(os.getenv("MONGOHOST"), int(os.getenv("MONGOPORT")))
    connection.register([Week])
    update_sheets(all_sheets, connection, Week, False, start_sheet=input("start_sheet: "), start_row=input("start_row: "))