<template>
  <div class="upload-form">
    <h5>File</h5>
    <b-form v-if="show">
        <b-row>
          <b-col>
            <b-form-group id="InputGroup"
                          label-for="dataInput">
              <b-form-file v-model="form.file"
                          id="dataInput"
                          :placeholder="selectedType == 'model_data' ? 'Select parameter file...' : 'Select a file...'"
                          description="Upload Image (.png .jpg .jpeg, size &lt; 200K)"
                          required
                          class="mt-3">
              </b-form-file>
            </b-form-group>
            <b-card v-if="form.file">
              <b-row class="mb-2">
                <b-col sm="3" class="text-sm-right"><b>File Size:</b></b-col>
                <b-col>{{ form.file.size }} bytes</b-col>
              </b-row>
              <b-row class="mb-2">
                <b-col sm="3" class="text-sm-right"><b>File Type:</b></b-col>
                <b-col>{{ form.file.type }}</b-col>
              </b-row>
              <b-row class="mb-2">
                <b-col sm="3" class="text-sm-right"><b>Last Modified:</b></b-col>
                <b-col>{{ new Date(form.file.lastModified).toJSON().slice(0, 19).replace('T', ' ') }}</b-col>
              </b-row>
            </b-card>
          </b-col>
          <b-col v-if="selectedType == 'model_data'">
            <b-form-group id="InputGroup2"
                          label-for="dataInput2">
              <b-form-file v-model="form.file2"
                          id="dataInput2"
                          placeholder="Select model data file..."
                          description="Upload Image (.png .jpg .jpeg, size &lt; 200K)"
                          required
                          class="mt-3">
              </b-form-file>
            </b-form-group>
          <b-card v-if="form.file2">
            <b-row class="mb-2">
              <b-col sm="3" class="text-sm-right"><b>File Size:</b></b-col>
              <b-col>{{ form.file2.size }} bytes</b-col>
            </b-row>
            <b-row class="mb-2">
              <b-col sm="3" class="text-sm-right"><b>File Type:</b></b-col>
              <b-col>{{ form.file2.type }}</b-col>
            </b-row>
            <b-row class="mb-2">
              <b-col sm="3" class="text-sm-right"><b>Last Modified:</b></b-col>
              <b-col>{{ new Date(form.file2.lastModified).toJSON().slice(0, 19).replace('T', ' ') }}</b-col>
            </b-row>
          </b-card>
        </b-col>
      </b-row>
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
    <h5>Data</h5>
    <b-table striped hover small :fields="fields" :items="items" class="transaction_table" v-if="items.length > 0">
      <template slot="hash" slot-scope="row">
        <p class="transaction_table_item" @click="row.toggleDetails">
        {{ row.item.hash }}
        </p>
      </template>
      <template slot="contractAddress" slot-scope="row">
        <p class="transaction_table_item" @click="row.toggleDetails">
        {{ row.item.contractAddress }}
        </p>
      </template>
      <template slot="row-details" slot-scope="row">
        <b-card>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Block Hash:</b></b-col>
            <b-col>{{ row.item.blockHash }}</b-col>
          </b-row>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Block Number:</b></b-col>
            <b-col>{{ row.item.blockNumber }}</b-col>
          </b-row>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Transaction Hash:</b></b-col>
            <b-col>{{ row.item.hash }}</b-col>
          </b-row>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Transaction Index:</b></b-col>
            <b-col>{{ row.item.transactionIndex }}</b-col>
          </b-row>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>From:</b></b-col>
            <b-col>{{ row.item.from }}</b-col>
          </b-row>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Gas Used:</b></b-col>
            <b-col>{{ row.item.gasUsed }}</b-col>
          </b-row>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Contract Address:</b></b-col>
            <b-col>{{ row.item.contractAddress }}</b-col>
          </b-row>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Status:</b></b-col>
            <b-col>{{ row.item.status ? 'Success' : 'Fail' }}</b-col>
          </b-row>
          <b-button size="sm" @click="row.toggleDetails">Hide Details</b-button>
        </b-card>
      </template>
    </b-table>
    <h5 v-else class="transaction_table none"> No record </h5>
  </div>
</template>

<script>
import * as RLP from "rlp";
import bus from "@/components/bus";
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
    const listdata = [
      hash,
      jsondata["RawSize"],
      jsondata["InputShape"],
      jsondata["OutputShape"],
      jsondata["Gas"],
      addr
    ];
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
      user: {
        name: "",
        key: null
      },
      form: {
        file: null,
        sender: this.web3.eth.coinbase,
        recipient: null
      },
      selectedType: "input_data",
      show: true,
      items: [],
      fields: [
        {
          label: "Block Number",
          key: "blockNumber"
        },
        {
          label: "File Type",
          key: "type"
        },
        {
          label: "File Size",
          key: "size"
        },
        {
          label: "Transaction Hash",
          key: "hash"
        },
        {
          label: "Contract Address",
          key: "contractAddress"
        }
      ]
    };
  },
  methods: {
    async onSubmit(evt) {
      var formdata = new FormData();

      if (this.selectedType == "input_data") {
        formdata.append("file", this.form.file);
      } else {
        formdata.append("params_file", this.form.file);
        formdata.append("json_file", this.form.file2);
      }
      var parma = {
        type: this.selectedType,
        author: this.web3.eth.defaultAccount
      };
      formdata.append(
        "json",
        new Blob([JSON.stringify(parma)], { type: "application/json" })
      );
      let response = await this.$http.post(
        "http://192.168.5.11:5002/txion",
        formdata,
        { emulateJSON: true }
      );
      let payload;
      if (this.selectedType == "model_data") {
        payload = "0x0001" + serializeModelData(response.body.info);
      } else {
        payload = "0x0002" + serializeInputData(response.body.info);
      }
      const sender = this.web3.eth.defaultAccount;

      let transaction = {
        to: null,
        from: sender,
        gasPrice: 1000000000,
        gas: 2100000,
        value: 0,
        data: payload
      };
      transaction.gasPrice = await this.web3.eth.getGasPrice();
      transaction.gas = await this.web3.eth.estimateGas({ data: payload });
      const receipt = await this.web3.eth.sendTransaction(
        transaction,
        async (err, hash) => {
          transaction = await this.web3.eth.getTransaction(hash);
          this.items.push({
            type: this.selectedType,
            size: this.form.file.size,
            timestamp: this.form.file.lastModified,
            hash: transaction.hash,
            blockNumber: "",
            contractAddress: ""
          });
          this.form.file = null;
        }
      );
      const item = this.items.find(d => d.hash == transaction.hash);
      item.blockNumber = receipt.blockNumber;
      item.blockHash = receipt.blockHash;
      item.gasUsed = receipt.gasUsed;
      item.from = receipt.from;
      item.status = receipt.status;
      item.transactionIndex = receipt.transactionIndex;
      item.contractAddress = receipt.contractAddress.toLowerCase();
      formdata = new FormData();
      var parma = {
        type: this.selectedType,
        author: this.web3.eth.defaultAccount
      };
      formdata.append(
        "json",
        new Blob([JSON.stringify(item)], { type: "application/json" })
      );
      response = await this.$http.post(
        "http://192.168.5.11:5002/api/data/upload",
        formdata,
        { emulateJSON: true }
      );
    },
    onReset(evt) {
      evt.preventDefault();
      this.form.sender = "";
      this.form.recipient = null;
      this.form.file = null;
      this.form.file2 = null;
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    }
  },
  watch: {
    items(val) {
      bus.$emit('data_update', val);
    }
  },
  async mounted() {
    var formdata = new FormData();
    var parma = {
      type: "all",
      from: this.web3.eth.defaultAccount.toLowerCase()
    };
    formdata.append(
      "json",
      new Blob([JSON.stringify(parma)], { type: "application/json" })
    );
    const response = await this.$http.post(
      "http://192.168.5.11:5002/api/data/list",
      formdata,
      { emulateJSON: true }
    );
    this.items = response.body.info;
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.transaction_table_item {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  max-width: 300px;
}

.transaction_table.none {
  text-align: center;
  padding: 2em;
  color: #a0a0a0;
}
</style>
