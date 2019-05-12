<template>
  <el-form
    ref="resetPassword"
    v-loading="loading"
    :model="resetPassword"
    :rules="resetPasswordRules"
    label-width="100px"
    label-suffix="："
    size="small"
    :disabled="loading"
    @submit.native.prevent
  >
    <el-form-item
      prop="password"
      label="新密码"
    >
      <el-input
        v-model="resetPassword.password"
        v-loading="passwordLoading"
        type="password"
        maxlength="30"
        :disabled="passwordLoading"
        placeholder="必填，长度8~30位，不得使用纯数字或常见密码"
        show-password
      />
    </el-form-item>
    <el-form-item>
      <el-button
        type="primary"
        native-type="submit"
        @click="onSubmit"
      >
        提交
      </el-button>
      <el-button
        type="plain"
        @click="$emit('cancel')"
      >
        取消
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import '../../../plugins/element.js'

export default {
  name: 'UserPasswordReset',
  props: {
    ids: {
      required: true,
      type: Array
    },
  },
  data() {
    let validatePassword = (rule, value, callback) => {
      this.passwordLoading = true
      this.$axios.post('/api/admin/password', {
        password: value
      }).then((response) => {
        if (response.data['can_use'] === true) {
          callback()
        } else {
          callback(new Error('密码过于常见，请使用强度更高的密码'))
        }
      }).catch(() => {
        this.$message.error('无法连接到服务器，请检查网络后重试！')
        callback(new Error('密码检验失败，请重新尝试'))
      }).then(() => {
        this.passwordLoading = false
      })
    }
    return {
      loading: false,
      resetPassword: {
        password: '',
      },
      resetPasswordRules: {
        password: [
          {required: true, message: '该项为必填项', trigger: 'blur'},
          {min: 8, message: '至少8位密码长度', trigger: 'blur'},
          {max: 30, message: '最多30位密码长度', trigger: 'blur'},
          {pattern: '\\D', message: '密码不能为纯数字', trigger: 'blur'},
          {validator: validatePassword, trigger: 'blur'},
        ],
      },
      passwordLoading: false,
    }
  },
  methods: {
    onSubmit() {
      this.$refs['resetPassword'].validate((valid) => {
        if (valid && !this.loading) {
          this.loading = true
          this.$axios.patch('/api/admin/users', {
            ids: this.ids,
            password: this.resetPassword['password']
          }).then(() => {
            this.$message.success('密码重置成功！')
            this.$emit('success')
          }).catch(() => {
            this.$message.error('无法连接到服务器，请检查网络后重试！')
          }).then(() => {
            this.loading = false
          })
        }
      })
    }
  }
}
</script>

<style>
</style>