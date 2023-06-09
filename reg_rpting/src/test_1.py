import re

#log_str='EVENT PID:141462 TID:140147300110784 09/06 11:20:20.689550 Logging.cpp 374 <<SENT_ATS_SOLACE<<  msgFixOrderReplaced MSG_SIZE=145  Sequence=1567738803676073  TO=/MemberOrderStreaming/SEE/HUSQb.SEE {member_order_id=457543720  target_quantity=150731  price=77.4  cl_ord_id=HUSQb.ST.eurgf.b918  oats_order_id=HUSQb.ST.eurgf.b918  min_execution_size=19  recurring_min_execution_size=19  price_instruction=0  market_instructions=L  order_replaced_time_utc_micros=1567765220689394  can_cross_slpioc=false  can_cross_slpday=true  can_cross_internal=true  pass_through_fields=  market_data_snapshot { bid=77.38  is_bid_slow=false  ask=77.46  is_ask_slow=false  mid=77.419999999999987  sip_upd_time=0  bridge_received_upd_time=1567765220650383228  nbbo_source=NBBO_SOURCE_REUTERS  } in_the_market=true  external_parent_quantity=200000  order_capacity= }'
# my_delimiter='  '
# print('log_str=', log_str)
# regex_extractpattern = re.compile(r"EVENT.*? TID:(.*?) (\d{2}/\d{2}) (\d{2}:\d{2}:\d{2}.\d{6}).*<<(.*?)<<  (msgFixOrderReplaced).*?Sequence=(.*?)  TO=(.*?) {member_order_id=(.*?)  target_quantity=(.*?)  price=(.*?)  cl_ord_id=(.*?) .*")
# x_str=re.findall(regex_extractpattern, log_str)
# # print(re.split('  ', log_str))
# print(x_str)



my_list = [1, 2, 3, 'example', 3.132, 10, 30]
for element in my_list: #access elements one by one
    print(element)
print(my_list) #access all elements
print(my_list[3]) #access index 3 element
print(my_list[0:2]) #access elements from 0 to 1, this EXCLUDES 2
print(my_list[::-1]) #access elements in reverse

