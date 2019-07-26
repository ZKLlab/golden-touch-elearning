<template>
  <el-form
    ref="courseCreate"
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
      />
    </el-form-item>
    <el-form-item
      label="课程简称"
      prop="addr"
    >
      <el-input
        v-model.trim="courseCreateForm.addr"
      />
    </el-form-item>
    <el-form-item
      label="课程英文别名"
      prop="slug"
    >
      <el-input
        v-model.trim="courseCreateForm.slug"
        placeholder="只能填写小写英文字母(a-z)和中划线(-)，中划线不能放在首尾"
      />
    </el-form-item>
    <el-form-item
      label="课程类别"
      prop="category"
    >
      <el-select
        v-model.trim="courseCreateForm.category"
        :value="courseCreateForm.category"
        placeholder="请选择或输入新类别名"
        no-data-text="输入新的类别名"
        filterable
        allow-create
      />
    </el-form-item>
    <el-form-item>
      <el-button
        type="primary"
        native-type="submit"
      >
        创建课程
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: 'CourseCreate',
  data() {
    return {
      courseCreateForm: {
        name: '',
        addr: '',
        slug: '',
        category: ''
      },
      courseCreateFormRule: {
        name: [
          {required: true, message: '此项为必填项', trigger: 'blur'}
        ],
        addr: [
          {required: true, message: '此项为必填项', trigger: 'blur'}
        ],
        slug: [
          {required: true, message: '此项为必填项', trigger: 'blur'},
          {pattern: '^[a-z|-]*$', message: '只能填写小写英文字母(a-z)和中划线(-)', trigger: 'blur'},
          {pattern: '^([a-z][a-z|-]*[a-z]|[a-z])$', message: '中划线不能放在首尾', trigger: 'blur'}
        ],
        category: [
          {required: true, message: '此项为必填项', trigger: 'change'}
        ]
      }
    }
  }
}
</script>

<style scoped>

</style>