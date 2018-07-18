<template>
  <div class="upload-form">
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="InputGroup1"
                    label="Sender:"
                    label-for="senderAddrInput"
                    description="We'll never share your address with anyone else.">
        <b-form-input id="senderAddrInput"
                      type="text"
                      v-model="form.sender"
                      disabled
                      placeholder="Enter address">
        </b-form-input>
      </b-form-group>
      <!--
      <b-form-group id="InputGroup2"
                    label="Recipient:"
                    label-for="recipientAddrInput">
        <b-form-input id="recipientAddrInput"
                      type="text"
                      v-model="form.recipient"
                      placeholder="Enter address">
        </b-form-input>
      </b-form-group>
      !-->
      <b-form-group id="InputGroup3"
                    label="Contract:"
                    label-for="contractInput">
        <b-form-textarea id="contractInput"
                      type="text"
                      v-model="form.contract"
                      disabled
                      placeholder="Enter contract">
        </b-form-textarea>
      </b-form-group>
      <b-form-group id="InputGroup4"
                    label="Model data:"
                    label-for="modelInput">  
        <b-input-group>
          <b-form-input id="modelInput"
                        type="text"
                        v-model="form.model_addr"
                        placeholder="Enter model data address">
          </b-form-input>
          <b-dropdown text="select" variant="outline-secondary" slot="append" right>
            <b-dropdown-item :key="item.hash" v-for="item in model_data" @click="form.model_addr = item.contractAddress">
              {{ item.contractAddress }}
            </b-dropdown-item>
          </b-dropdown>
        </b-input-group>
      </b-form-group>
      <b-form-group id="InputGroup5"
                    label="Input data:"
                    label-for="dataInput">
        <b-input-group>
          <b-form-input id="dataInput"
                        type="text"
                        v-model="form.input_addr"
                        placeholder="Enter input data address">
          </b-form-input>
          <b-dropdown text="select" variant="outline-secondary" slot="append" right>
            <b-dropdown-item :key="item.hash" v-for="item in input_data" @click="form.input_addr = item.contractAddress">
              {{ item.contractAddress }}
            </b-dropdown-item>
          </b-dropdown>
        </b-input-group>
      </b-form-group>
      <b-button type="submit" variant="primary">Call</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <hr class="my-4">
    <b-card>
      {{ result }}
    </b-card>
  </div>
</template>

<script>
import * as RLP from "rlp";
import { Buffer } from "safe-buffer";
import { promisify } from "es6-promisify";
import bus from "@/components/bus";

function parseHexString(str) {
  var result = [];
  for (var i = 0; i < str.length; i += 2) {
    result.push(parseInt(str.substring(i, i + 2), 16));
  }
  return Buffer.from(result);
}

function createHexString(arr) {
  const str = "0123456789abcdef";
  return "".concat(...Array.from(arr).map(d => "" + str[d >> 4] + str[d & 15]));
}

function createPayload(jsondata) {
  let ret = "";
  try {
    const addrBytes = Buffer.from(jsondata["AuthorAddress"]);
    const addr = addrBytes.slice(addrBytes.length - 20);
    const hash = parseHexString(jsondata["Hash"].slice(2));
    const listdata = [hash, jsondata["RawSize"], jsondata["Shape"], addr];
    ret = createHexString(RLP.encode(listdata));
  } catch (e) {}
  return ret;
}

export default {
  name: "CallContractView",
  data() {
    return {
      result: null,
      input_data: [],
      model_data: [],
      form: {
        file: null,
        sender: this.web3.eth.defaultAccount.toLowerCase(),
        recipient: null,
        contract: `contract DemoSmartContract { 
  mapping(address=>uint) account;

  //other code
  ....
 
  //classify type of picture
  function animalClassification(address input, address model){
    //get infer result
    var result = keccak256(infer(input, model));

    //reward according to your choice
    if (result == keccak256("bird"))
      account[msg.sender] += 10
  }

  //other code
  ....
}
	`,
        model_addr: null,
        input_addr: null,
      },
      show: true
    };
  },
  mounted() {
    bus.$on('data_update', (val) => {
      this.input_data = val.filter(d => d.type == 'input_data');
      this.model_data = val.filter(d => d.type == 'model_data');
    });
  },
  methods: {
    async onSubmit(evt) {
      var formdata = new FormData();
      var parma = { input_addr: form.input_addr, model_addr: form.model_addr };
      formdata.append("json", new Blob([JSON.stringify(parma)], { type: "application/json" }));
      const response = await this.$http.post(
        "http://192.168.5.11:5002/infer",
        formdata,
        { emulateJSON: true }
      );
      this.result = response;
    },
    onReset (evt) {
      evt.preventDefault();
      /* Reset our form values */
      this.form.sender = '';
      this.form.recipient = null;
      this.form.file = null;
      this.show = false;
      this.$nextTick(() => { this.show = true });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
