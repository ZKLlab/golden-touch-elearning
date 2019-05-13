<template>
  <el-form
    ref="login"
    v-loading="loading"
    :model="login"
    :rules="loginRules"
    :disabled="loading"
    label-position="left"
    label-width="0"
    hide-required-asterisk
    @submit.native.prevent
  >
    <el-form-item prop="username">
      <el-input
        v-model="login.username"
        type="text"
        placeholder="用户名"
        prefix-icon
      >
        <font-awesome-icon
          slot="prefix"
          class="icon-prefix"
          icon="user"
        />
      </el-input>
    </el-form-item>
    <el-form-item prop="password">
      <el-input
        v-model="login.password"
        type="password"
        placeholder="密码"
      >
        <font-awesome-icon
          slot="prefix"
          class="icon-prefix"
          icon="key"
        />
      </el-input>
    </el-form-item>
    <div class="action">
      <el-button
        type="primary"
        native-type="submit"
        @click="onLogin"
      >
        登录
      </el-button>
    </div>
  </el-form>
</template>

<script>
import '../plugins/element.js'
import '../plugins/fontawesome.js'

export default {
  name: 'LoginBox',
  data() {
    return {
      login: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{required: true, message: '请输入用户名', trigger: 'blur'}],
        password: [{required: true, message: '请输入密码', trigger: 'blur'}]
      },
      loading: false,
    }
  },
  methods: {
    onLogin() {
      this.$refs['login'].validate((valid) => {
        if (valid && !this.loading) {
          this.loading = true;
          this.$axios.post('/api/session', {
            username: this.login.username,
            password: this.login.password
          }).then(() => {
            this.$refs['login'].resetFields()
            this.$store.dispatch('updateUserInfo')
            this.$message({
              message: '登录成功！',
              type: 'success'
            })
            this.$emit('login-success')
          }).catch((error) => {
            if (error.response) {
              if (error.response.status === 400) {
                this.$message.error('用户名或密码错误！')
              }
            } else {
              this.$message.error('无法连接到服务器，请检查网络后重试！')
            }
          }).then(() => {
            this.loading = false
          })
        }
      })
    }
  }
}
</script>

<style scoped>
  .action {
    text-align: center;
  }

  .icon-prefix {
    margin-left: 5px;
  }
</style>