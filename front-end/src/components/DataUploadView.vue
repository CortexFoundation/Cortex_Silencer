<template>
  <div class="upload-form">
    <b-form v-if="show">
      <b-form-group id="InputGroup"
                    label="Select file to upload:"
                    label-for="dataInput">
        <b-form-file v-model="form.file"
                    id="dataInput"
                    placeholder="Select a file..."
                    description="Upload Image (.png .jpg .jpeg, size &lt; 200K)"
                    required
                    class="mt-3">
        </b-form-file>
      </b-form-group>
      <b-form-group>
        <b-form-radio-group id="TypeRadios" v-model="selectedType" name="radioSubComponent">
          <b-form-radio value="input_data">Input data</b-form-radio>
          <b-form-radio value="model_data">Model data</b-form-radio>
        </b-form-radio-group>
      </b-form-group>
      <b-button @click="onSubmit" variant="primary">Upload</b-button>
      <b-button @click="onReset" variant="danger">Reset</b-button>
    </b-form>
    <hr class="my-4">
    <h5>Data / Model</h5>
    <b-table striped hover :fields="fields" :items="items"></b-table>
  </div>
</template>

<script>
import * as RLP from "rlp";
import { Buffer } from "safe-buffer";
import { promisify } from "es6-promisify";

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

function serializeModelData(jsondata) {
  let ret = "";
  try {
    const addrBytes = Buffer.from(jsondata["AuthorAddress"]);
    const addr = addrBytes.slice(addrBytes.length - 20);
    const hash = parseHexString(jsondata["Hash"].slice(2));
    const listdata = [hash, jsondata["RawSize"], jsondata["InputShape"], jsondata["OutputShape"], jsondata["Gas"], addr];
    ret = createHexString(RLP.encode(listdata));
  } catch (e) {}
  return ret;
}

function serializeInputData(jsondata) {
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
  name: "DataUploadView",
  data() {
    return {
      form: {
        file: null,
        sender: this.web3.eth.coinbase,
        recipient: null,
      },
      selectedType: 'input_data',
      show: true,
      items: [],
      fields: ['Type', 'Transaction Hash', 'Block Number', 'Contract Address'],
    };
  },
  methods: {
    async onSubmit(evt) {
      var formdata = new FormData();
      formdata.append("file", this.form.file);
      var parma = { type: this.selectedType, author: web3.eth.defaultAccount };
      formdata.append("json", new Blob([JSON.stringify(parma)], { type: "application/json" }));
      const response = await this.$http.post("http://192.168.5.11:5000/txion", formdata, {emulateJSON: true});
      let payload;
      if (this.selectedType == "model_data") {
        payload = "0x0001" + serializeModelData(response.body.info);
      } else {
        payload = "0x0002" + serializeInputData(response.body.info);
      }
      const sender = this._web3.eth.defaultAccount;

      let transaction = {
        to: null,
        from: sender,
        gasPrice: 1000000000,
        gas: 2100000,
        value: 0,
        data: payload,
      };
      transaction.gasPrice = await this.web3.eth.getGasPrice();
      transaction.gas = await this.web3.eth.estimateGas({data: payload});

      const receipt = await this.web3.eth.sendTransaction(transaction, async (err, hash) => {
        transaction = await this.web3.eth.getTransaction(hash);
        this.items.push({
          'Type': parma.type == 'model_data' ? 'model' : 'input',
          'Transaction Hash': transaction.hash,
          'Block Number': '',
          'Contract Address': '',
        });
      });
      const item = this.items.find((d) => d['Transaction Hash'] == transaction.hash);
      item['Block Number'] = receipt.blockNumber;
      item['Contract Address'] = receipt.contractAddress;
    },
    onReset (evt) {
      evt.preventDefault();
      /* Reset our form values */
      this.form.sender = '';
      this.form.recipient = null;
      this.form.file = null;
      this.show = false;
      this.$nextTick(() => { this.show = true });
    },
    getTransactionReceipt(data) {
      this.web3.eth.getTransactionReceipt(data.transaction.hash, (err, receipt) => {
        data.receipt = receipt;
      });
    },
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.upload-form {
  width: 100%;
  margin-top: 2em;
  margin-bottom: 2em;
}

.form-content {
  width: 100%;
  box-shadow: 0 10px 30px rgba(0,0,0,0.6);
}

.form-message {
  margin-top: 2em;
  margin-bottom: 2em;
}

.custom-file-label {
  border-color: lightgray !important;
}

.b-form-file {
  margin-bottom: 1em;
}
.b-form-group {
  margin-top: 2em;
}

</style>
