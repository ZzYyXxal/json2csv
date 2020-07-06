# *_*coding:utf-8 *_*
import json
import csv
class Json2csvTransformer():
    """
    a transformer that can transform json file to corresponding csv file.
    if there are dictionaries in  the keys of json,like {'name':jack,'feature':{'birthday':1901.1.1}},
    the corresponding result will be feature_birthday
    if there are comma in the values if json,like {url_list:[url0,url1,url2]}
    the result will be {url_list_0:url0,url_list_1:url1,url_list_2:url2}
    """
    def __init__(self,json_filename=r"../../json2csv/json/person.json"
                 ,csv_filename=r"../../json2csv/csv/person.csv"):
        """
        initial Json2csvTransformer
        :param json_filename:the json file that needs to be converted to csv file
        :param csv_filename:the conversion result
        """
        self.json_filename=json_filename
        self.csv_filename=csv_filename
        self.json_data={}
        self.keys_set=set()
        self.csv_result=[]
        json_file_ptr=open(json_filename,'r',encoding='utf-8')
        json_file=json_file_ptr.read()
        json_file_ptr.close()
        #去除utf-8 BOM
        if json_file.startswith(u'\ufeff'):
            json_file = json_file.encode('utf8')[3:].decode('utf8')
        json_file=json_file[:-3]+json_file[-2:] #去除结尾逗号
        self.json_data = json.loads(json_file)

    def get_dict(self,per_dict,key,value):
        """
        recursively concatenate to get keys and values
        :param key:
        :param value:
        :return:
        """
        for sub_key,sub_value in value.items():
            new_key=key+'_'+sub_key
            if (isinstance(sub_value, dict)):
                self.get_dict(per_dict, new_key, sub_value)
            elif (isinstance(sub_value, list)) or (isinstance(sub_value, tuple)):
                self.get_list(per_dict, new_key, sub_value)
            else:
                self.keys_set.add(new_key)
                per_dict[new_key] = sub_value

    def get_list(self, per_dict, key, value):
        """
        recursively concatenate to get keys and values
        :param key:
        :param value:
        :return:
        """
        index =0
        for item in value:
            index=index+1
            str_index="%03d"%index
            new_key=key+'_'+str_index
            if (isinstance(item, dict)):
                self.get_dict(per_dict, new_key, item)
            elif (isinstance(item, list)) or (isinstance(item, tuple)):
                self.get_list(per_dict, new_key, item)
            else:
                self.keys_set.add(new_key)
                per_dict[new_key] = item

    def read_keys(self):
        """
        traverse the json data,  gather all the keys
        :return:
        """
        for json_data_item in self.json_data:
            per_dict={}
            for key,value in json_data_item.items():
                if(isinstance(value,dict)):
                    self.get_dict(per_dict,key,value)
                elif(isinstance(value,list)) or (isinstance(value,tuple)):
                    self.get_list(per_dict,key,value)
                else:
                    self.keys_set.add(key)
                    per_dict[key]=value
            self.csv_result.append(per_dict)

    def translate(self):
        """
        translater
        :return:
        """
        self.read_keys()
        keys_list=sorted(self.keys_set)
        #这里的编码utf-8-sig是为了解决csv中的字段值中含有逗号导致乱码问题
        #参见https://www.cnblogs.com/qiaoer1993/p/12604509.html
        #import csv
        #with open("baiyibutie.csv", "a", encoding="utf-8-sig",
        #       newline="") as fp:  # 标红的参数是为了解决用excel打开乱码的问题，加上这个参数后用excel打开就会正常显示，不会乱码
        #    fieldnames = ['name', 'price', 'cate', 'url', 'data']  # 这是标题栏的内容
        #    writer = csv.DictWriter(fp, fieldnames=fieldnames)  # 把标题栏加入到csv文件中
        #    writer.writeheader()  # 这一行是写入第一行的标题栏，放在for循环的外面，不然就会出现很多个标题栏
        #   writer.writerow(
        #       {'name': result["shortName"], 'price': price, 'cate': cate, 'url': "http:" + result["itemUrl"], 'data':

        # csv_file=open(self.csv_filename,"w+",encoding="utf-8-sig")
        # csv_file.write(','.join(['"'+i+'"' for i in keys_list]) + '\n')
        # for per in self.csv_result:
        #     per_line=[]
        #     for item in keys_list:
        #         if item in per:
        #             per_line.append('"'+per[item]+'"')
        #         else:
        #             per_line.append('""')
        #     csv_file.write(','.join(per_line) + '\n')
        # csv_file.close()

        csv_file = open(self.csv_filename, "w+", encoding="utf-8-sig",newline="")
        writer = csv.DictWriter(csv_file, fieldnames=keys_list)
        writer.writeheader()
        for per in self.csv_result:
            writer.writerow(per)
        csv_file.close()

if __name__ == '__main__':
    json2csv=Json2csvTransformer()
    json2csv.translate()
    # filename=r"../../json2csv/json/person.json"
    # fp= open(filename,'w+',encoding='utf-8')