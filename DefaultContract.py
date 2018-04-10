#this instruction is for specific contract "Default Contract"
# contract DefaultContract{ 
#  mapping(address=>uint) account;

#  //other code
#  ....
 
#  //classify type of picture
#  function animalClassification(address input, address model){
#   //get infer result
#   var result = keccak256(infer(input, model));

#   //reward according to your choice
#   if (result == keccak256("hummingbird"))
#    account[msg.sender] += 10
#   else if (result == keccak256("standard schnauzer")) //standard schnauzer is dog
#    account[msg.sender] += 5
#   else if (result == keccak256("tabby, tabby cat"))
#    account[msg.sender] += 1
#     }
#  //other code
#  ....
# }
def Run(account,tx,CVM):
    tx["amount"] = 0
    tx["comment"] = CVM.inference("./model_bind/"+t["model"], "./input_data/"+t["input"])
    if tx["comment"] == "standard schnauzer":
        account[tx["from"]]+=5
        tx["amount"] = 5
    if tx["comment"] == "hummingbird":
        account[tx["from"]]+=10
        tx["amount"] = 10
    if tx["comment"] == "tabby, tabby cat":
        account[tx["from"]]+=1
        tx["amount"] = 1