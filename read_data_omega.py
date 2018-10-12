import sys
import datetime
import requests
import json
import os

host="http://localhost:9200"
url_stock = host + "/pk/stock"
url_price = host + "/pk/price"
separator = '\x01'

def main(args):
   print(args)
   if len(args) < 3 :
       print ("Usage : " + args[0] + " <price|stock> <date> ")
       exit()
   
   #default values
   check_type = "price"
   check_date = datetime.datetime.today().strftime('%Y%m%d')
 
   if args[1] == "stock" :
      check_type = "stock"
   if args[2] != check_date :
      check_date = args[2]

   load_data(check_type, check_date)
   

def load_data(check_type, check_date):
    file_name = check_type + "_" + str(check_date) +".txt"
    if os.path.exists(file_name) == True:
	    f = open(file_name,"r+")
	    if check_type == "stock" :
	        url = url_stock
	    else :
	        url = url_price


	    print("url = {} \n".format(url))
	    data = ""
	    document_id = ""
	    
	    base_url = url 
	    for line in f:
	        #print line
	        columns = line.rstrip().split(separator)
	        if check_type == "stock" :
	            data = {"tanggal": str(columns[0]), "nama_cabang" : str(columns[1]), "kode_barang" : str(columns[2]), "stock_aktif" : float(columns[3]) }
	            document_id = str(columns[2]) +"_" + str(check_date)
	        else : 
	            data = {"tanggal": str(columns[0]), "kode" : str(columns[1]), "barang": str(columns[2]), "harga":float(columns[3])}
	            document_id = str(columns[1]) + "_" + str(check_date)

	        #print(data)
	        url = url + "/" + document_id
	        print(url)
	        r = requests.post(url,data = json.dumps(data))
	        #print(r.status)
	        url = base_url

	    f.close()



 
      


if __name__ == "__main__" :
    main(sys.argv)

import requests
import json
import datetime
import sys

def main():
   #print "Hello jacki requests"
   endpoint_price = "http://omegasoft.co.id/dev-api-e-commerce/price.php"
   endpoint_stock = "http://omegasoft.co.id/dev-api-e-commerce/stock.php"
  
   token = "9eeb7e2b9e5c48308256224e6d97a02f"
   uid = "1e6ad554c5b64d038855d0de155dcce3"
   
     
   #assign default value
   last_check = datetime.datetime.today().strftime('%Y%m%d')
   url = endpoint_price
   file_name = "price"
   check = "price"

   #check arguments
   if (len(sys.argv) < 2 ) : 
       #print usage
       print("Usage : " + sys.argv[0] + " [price|stock] [date] ")
       print("arguments : date - YYYYMMDD ; default today's date")
       print("          : price|stock ; default price")
       exit()
   else :
       last_check = str(sys.argv[2])
       if (sys.argv[1] == "stock") :
           url = endpoint_stock
           file_name = "stock"
           check = "stock"


       
       


   data  = {'token' : token, "uid" : uid, "last_check" : last_check}
   r = get_data(url, data)
   print(r.text)
   
   dict_data = json.loads(r.text.replace(',,',','))
   print(dict_data['databarang'])

   entry = last_check 

   '''
   for barang in dict_data['databarang'] :
       for k,v in barang.items():
           entry = ";".join([entry,k + ":" + v])    
       entry = entry + "\n"
       print (entry)
       entry = last_check
   '''
   file_name = file_name + "_" + last_check + ".txt"

   fout = open(file_name,"w")
   last_update = last_check[0:4] + "/" + last_check[4:6] + "/" + last_check[6:] 
   if check == "stock" :
       write_stock_update(dict_data,fout,last_update)
   else :
       write_price_update(dict_data,fout,last_update)


def write_price_update(dict_data,file_handler,last_check):
   separator = "\x01" 
   for barang in dict_data['databarang']:
      entry = separator.join([last_check,barang["Barang"],barang["Keterangan"],barang["HargaJual"]])
      entry = entry 
      file_handler.write(entry + "\n")
      print(entry)

   file_handler.close()

def write_stock_update(dict_data,file_handler,last_check):
    separator = "\x01"
    for barang in dict_data['databarang']:
      entry = separator.join([last_check,barang["NAMACABANG"],barang["BARANG"],barang["STOKAKTIF"]])
      entry = entry 
      file_handler.write(entry + "\n")
      print(entry)
    file_handler.close()



def get_data(url,data):
    r = requests.post(url,data=data)
    return r


if __name__ == "__main__" :
    main()

