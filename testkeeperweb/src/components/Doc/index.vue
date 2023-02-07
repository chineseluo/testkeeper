<template>
  <div>
    <svg-icon icon-class="doc" @click="click" />
  </div>
</template>

<script>
export default {
  name: 'Doc',
  methods: {
    click() {
      window.open('http://127.0.0.1:5000/pages/010101/', '_blank')
    }
  }
}
</script>
