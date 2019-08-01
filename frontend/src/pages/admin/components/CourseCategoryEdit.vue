<template>
  <el-form
    ref="courseCategoryEdit"
    v-loading="loading"
    :model="courseCategoryEditForm"
    :rules="courseCategoryEditFormRule"
    label-width="160px"
    label-suffix="："
    size="small"
    @submit.native.prevent
  >
    <el-form-item
      label="课程类别"
      prop="category_name"
    >
      <el-select
        v-model.trim="courseCategoryEditForm.category_name"
        :value="courseCategoryEditForm.category_name"
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
  name: 'CourseCategoryEdit',
  props: {
    slug: {
      type: String,
      required: true,
    },
    originalCategoryName: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      courseCategoryEditForm: {
        category_name: this.originalCategoryName,
      },
      courseCategoryEditFormRule: {
        category_name: [
          {required: true, message: '此项为必填项', trigger: 'blur'},
        ],
      },
      categories: [],
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
      this.$refs['courseCategoryEdit'].validate((valid) => {
        if (valid && !this.loading) {
          this.loading = true
          this.$axios.patch(`/course/${this.slug}`, this.courseCategoryEditForm).then((response) => {
            this.$message.success('成功修改课程类别！')
            this.$emit('success', response.data['category'])
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