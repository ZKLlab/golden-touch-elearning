<template>
  <el-form
    ref="lessonNameEdit"
    v-loading="loading"
    :model="lessonNameEditForm"
    :rules="lessonNameEditFormRule"
    label-width="160px"
    label-suffix="："
    size="small"
    @submit.native.prevent
  >
    <el-form-item
      label="课程名称"
      prop="name"
    >
      <el-input
        v-model.trim="lessonNameEditForm.name"
        maxlength="80"
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
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: 'LessonNameEdit',
  props: {
    slug: {
      type: String,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
    originalName: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      lessonNameEditForm: {
        name: this.originalName,
      },
      lessonNameEditFormRule: {
        name: [
          {required: true, message: '此项为必填项', trigger: 'blur'}
        ],
      },
      loading: false,
    }
  },
  methods: {
    onSubmit() {
      this.$refs['lessonNameEdit'].validate((valid) => {
        if (valid && !this.loading) {
          this.loading = true
          this.$axios.patch(`/course/${this.slug}/lesson/${this.id}`, this.lessonNameEditForm).then((response) => {
            this.$message.success('成功修改课时名称！')
            this.$emit('success', response.data)
          }).catch(() => {
            this.$message.error('无法连接到服务器，请检查网络后重试！')
          }).then(() => {
            this.loading = false
          })
        }
      })
    },
  },
}
</script>

<style scoped>

</style>