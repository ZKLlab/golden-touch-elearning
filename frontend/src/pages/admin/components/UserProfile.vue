<template>
  <el-form
    ref="profile"
    v-loading="loading"
    :model="profile"
    :rules="profileRules"
    label-width="120px"
    label-suffix="："
    size="small"
    :disabled="loading"
    @submit.native.prevent
  >
    <el-form-item label="用户类型">
      <strong>{{ userTypeName }}</strong>
    </el-form-item>
    <el-form-item
      label="用户名"
      prop="username"
    >
      <el-input
        v-model.trim="profile.username"
        v-loading="usernameLoading"
        placeholder="必填，支持大小写字母、数字和部分符号（@/./+/-/_），长度≤150字节"
        :disabled="usernameLoading"
      />
    </el-form-item>
    <el-form-item
      :label="displayNameLabel"
      prop="display_name"
    >
      <el-input
        v-model.trim="profile.display_name"
        placeholder="必填，长度≤150字节"
      />
    </el-form-item>
    <el-form-item
      label="性别"
      prop="gender"
    >
      <el-radio-group v-model="profile.gender">
        <el-radio :label="2">
          男
        </el-radio>
        <el-radio :label="1">
          女
        </el-radio>
        <el-radio :label="0">
          不显示
        </el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item
      label="是否启用"
      prop="is_active"
    >
      <el-switch
        v-model="profile.is_active"
        :disabled="data === null ? false : data['is_current_user']"
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
        @click="resetForm"
      >
        重置
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import '../../../plugins/element.js'
import strLength from 'node-mb-string-size'

export default {
  name: 'UserProfile',
  props: {
    data: {
      type: Object,
      default: null
    },
    userType: {
      required: true,
      type: String,
      validator(value) {
        return ['volunteer', 'school', 'student'].indexOf(value) !== -1
      }
    },
    action: {
      required: true,
      type: String,
      validator(value) {
        return ['add', 'edit'].indexOf(value) !== -1
      }
    }
  },
  data() {
    let validateUsername = (rule, value, callback) => {
      if (this.data !== null && value === this.data['username']) {
        callback()
      } else {
        this.usernameLoading = true
        this.$axios.get('/username', {
          params: {u: value},
        }).then((response) => {
          if (response.data['can_use'] === true) {
            callback()
          } else {
            callback(new Error('用户名已被占用，请修改'))
          }
          this.usernameLoading = false
        }).catch((error) => {
          if (!this.$axios.isCancel(error)) {
            this.$message.error('无法连接到服务器，请检查网络后重试！')
            callback(new Error('用户名验证失败，请重新尝试'))
          }
        }).then(() => {
          this.usernameLoading = false
        })
      }
    }
    let validateLength = (len) => {
      return (rule, value, callback) => {
        if (strLength(value) > len) {
          callback(new Error(`长度需在${len}字节以内`))
        } else {
          callback()
        }
      }
    }
    return {
      profile: {
        display_name: this.data !== null ? this.data['display_name'] : '',
        username: this.data !== null ? this.data['username'] : '',
        is_active: this.data !== null ? this.data['is_active'] : true,
        gender: this.data !== null ? this.data['gender'] : 0,
      },
      profileRules: {
        username: [
          {required: true, message: '此项为必填项', trigger: 'blur'},
          {pattern: '^[\\w.@+-]+$', message: '只支持大小写字母、数字和部分符号(@/./+/-/_)', trigger: 'blur'},
          {validator: validateLength(150), trigger: 'blur'},
          {validator: validateUsername, trigger: 'blur'},
        ],
        display_name: [
          {required: true, message: '此项为必填项', trigger: 'blur'},
          {validator: validateLength(150), trigger: 'blur'},
        ],
        is_active: [],
        gender: []
      },
      usernameLoading: false,
      loading: false
    }
  },
  computed: {
    userTypeName() {
      return {student: '学生', school: '学校', volunteer: '志愿者'}[this.userType]
    },
    displayNameLabel() {
      return {student: '姓名', school: '名称', volunteer: '名字'}[this.userType]
    },
  },
  methods: {
    onSubmit() {
      this.$refs['profile'].validate((valid) => {
        if (valid && !this.loading) {
          this.loading = true
          if (this.action === 'add') {
            let profile = this.profile
            profile['user_type'] = this.userTypeID()
            this.$axios.post('/user', profile).then(() => {
              this.$message({
                message: '用户添加成功！',
                type: 'success',
              })
              this.$emit('success', false)
            }).catch(() => {
              this.$message.error('无法连接到服务器，请检查网络后重试！')
            }).then(() => {
              this.loading = false
            })
          } else {
            let profile = this.profile
            this.$axios.put(`/user/${this.data.id}`, profile).then(() => {
              this.$message.success('用户信息修改成功！')
              this.$emit('success', false)
            }).catch(() => {
              this.$message.error('无法连接到服务器，请检查网络后重试！')
            }).then(() => {
              this.loading = false
            })
          }
        }
      })
    },
    resetForm() {
      this.$confirm(this.action === 'add' ? '将表单重置到初始状态？' : '取消一切修改，并重置表单到修改前的状态？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(() => {
        this.$refs['profile'].resetFields()
      })
    },
    userTypeID() {
      return {student: 0, school: 1, volunteer: 2}[this.userType]
    },
  }
}
</script>

<style>
</style>