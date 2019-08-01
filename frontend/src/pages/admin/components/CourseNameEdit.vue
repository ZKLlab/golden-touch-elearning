<template>
  <el-form
    ref="courseNameEdit"
    v-loading="loading"
    :model="courseNameEditForm"
    :rules="courseNameEditFormRule"
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
        v-model.trim="courseNameEditForm.name"
        maxlength="80"
      />
    </el-form-item>
    <el-form-item
      label="课程简称"
      prop="abbr"
    >
      <el-input
        v-model.trim="courseNameEditForm.abbr"
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
  name: 'CourseNameEdit',
  props: {
    slug: {
      type: String,
      required: true,
    },
    originalName: {
      type: String,
      required: true,
    },
    originalAbbr: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      courseNameEditForm: {
        name: this.originalName,
        abbr: this.originalAbbr,
      },
      courseNameEditFormRule: {
        name: [
          {required: true, message: '此项为必填项', trigger: 'blur'}
        ],
        abbr: [
          {required: true, message: '此项为必填项', trigger: 'blur'}
        ],
      },
      loading: false,
    }
  },
  methods: {
    onSubmit() {
      this.$refs['courseNameEdit'].validate((valid) => {
        if (valid && !this.loading) {
          this.loading = true
          this.$axios.patch(`/course/${this.slug}`, this.courseNameEditForm).then((response) => {
            this.$message.success('成功修改课程名称！')
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