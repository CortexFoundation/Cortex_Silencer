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
        <b-form-input id="contractInput"
                      type="text"
                      v-model="form.contract"
                      disabled
                      placeholder="Enter contract">
        </b-form-input>
      </b-form-group>
      <b-form-group id="InputGroup4"
                    label="Model:"
                    label-for="modelInput">  
        <b-input-group>
          <b-form-input id="modelInput"
                        type="text"
                        v-model="form.model_addr"
                        disabled
                        placeholder="">
          </b-form-input>
          <b-dropdown text="select" variant="outline-secondary" slot="append" right disabled>
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
      <b-alert v-for="data in output_data"
              :key="data"
              dismissible
              fade
              variant="warning"
              @dismissed="output_data.splice(index, 1)" show>
          {{ `result: ${data}` }}
      </b-alert>
    </b-card>
  </div>
</template>

<script>
import * as RLP from "rlp";
import { Buffer } from "safe-buffer";
import { promisify } from "es6-promisify";
import bus from "@/components/bus";

export default {
  name: "CallContractView",
  data() {
    return {
      result: null,
      input_data: [],
      model_data: [],
      output_data: [],
      form: {
        file: null,
        sender: this.web3.eth.defaultAccount.toLowerCase(),
        recipient: null,
        contract: '0x599fcd26a4e2d2d73a4b4d20286ad68bf4fa0e00',
        model_addr: 'CallInfer.call',
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
      const payload =
        this.web3.utils.sha3('Call(address)').slice(0, 10) + '000000000000000000000000' + this.form.input_addr.slice(2);
      let transaction = {
        to: this.form.contract,
        from: this.form.sender,
        gasPrice: 1000000000,
        gas: 2100000,
        value: 0,
        data: payload
      };
      transaction.gasPrice = parseInt(await this.web3.eth.getGasPrice());
      // transaction.gas = await this.web3.eth.estimateGas({ data: payload, to: this.form.contract });
      const name = ~~(Math.random() * 10000);
      const receipt = await this.web3.eth.sendTransaction(transaction, (err, d) => {
        console.log(err, d);
      });
      let result = await this.web3.eth.call({
        from: this.form.sender,
        to: this.form.contract,
        data: this.web3.utils.sha3('GetLastResult()').slice(0, 10)
      });
      result = this.web3.utils.toDecimal(result);
      this.output_data.push(result);
      console.log(receipt);
    },
    onReset (evt) {
      evt.preventDefault();
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
