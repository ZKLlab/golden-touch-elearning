<template>
  <el-form
    ref="courseCreate"
    v-loading="loading"
    :model="courseCreateForm"
    :rules="courseCreateFormRule"
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
        v-model.trim="courseCreateForm.name"
        maxlength="80"
      />
    </el-form-item>
    <el-form-item
      label="课程简称"
      prop="abbr"
    >
      <el-input
        v-model.trim="courseCreateForm.abbr"
        maxlength="80"
      />
    </el-form-item>
    <el-form-item
      label="课程英文别名"
      prop="slug"
    >
      <el-input
        v-model.trim="courseCreateForm.slug"
        placeholder="只能填写小写英文字母(a-z)和中划线(-)，中划线不能放在首尾"
        maxlength="80"
      />
    </el-form-item>
    <el-form-item
      label="课程类别"
      prop="category_name"
    >
      <el-select
        v-model.trim="courseCreateForm.category_name"
        :value="courseCreateForm.category_name"
        placeholder="请选择或输入新类别名"
        no-data-text="输入新的类别名"
        filterable
        allow-create
      >
        <el-option
          v-for="category in categories"
          :key="category.name"
          :label="category.name"
          :value="category.name"
        />
      </el-select>
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
  name: 'CourseCreate',
  data() {
    return {
      categories: [],
      courseCreateForm: {
        name: '',
        abbr: '',
        slug: '',
        category_name: '',
      },
      courseCreateFormRule: {
        name: [
          {required: true, message: '此项为必填项', trigger: 'blur'}
        ],
        abbr: [
          {required: true, message: '此项为必填项', trigger: 'blur'}
        ],
        slug: [
          {required: true, message: '此项为必填项', trigger: 'blur'},
          {pattern: '^[a-z|-]*$', message: '只能填写小写英文字母(a-z)和中划线(-)', trigger: 'blur'},
          {pattern: '^([a-z][a-z|-]*[a-z]|[a-z])$', message: '中划线不能放在首尾', trigger: 'blur'}
        ],
        category_name: [
          {required: true, message: '此项为必填项', trigger: 'change'}
        ]
      },
      loading: true,
    }
  },
  mounted() {
    this.update()
  },
  methods: {
    update() {
      this.$axios.get('/course_categories').then((response) => {
        this.categories = response.data
      }).catch(() => {
        this.$message.error('无法连接到服务器，请检查网络后重试！')
      }).then(() => {
        this.loading = false
      })
    },
    onSubmit() {
      this.$refs['courseCreate'].validate((valid) => {
        if (valid && !this.loading) {
          this.loading = true
          this.$axios.post('/course', this.courseCreateForm).then((response) => {
            this.$message.success('课程添加成功')
            this.$emit('success', response.data['slug'])
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