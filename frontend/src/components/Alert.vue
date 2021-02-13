<template>
  <b-row>
    <b-col cols="6">
      <div>
        <br>
        <b-alert variant="success" show>{{ message }}</b-alert>
      </div>
    </b-col>
  </b-row>
</template>


<script>
  export default{
    props: ['message'],
    data(){
        return{
        }
    },
    methods: {
    }
  }
</script>
