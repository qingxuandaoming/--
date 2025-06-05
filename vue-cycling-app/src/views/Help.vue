<template>
  <main class="container">
    <div class="help-container">
      <div class="help-header">
        <h1>帮助中心</h1>
        <p>找到您需要的所有帮助和支持，让您的骑行体验更加顺畅</p>
      </div>
      
      <div class="help-search">
        <i class="fas fa-search"></i>
        <input type="text" v-model="searchQuery" placeholder="搜索您的问题...">
      </div>
      
      <div class="faq-categories">
        <div 
          v-for="(category, index) in categories" 
          :key="index"
          class="category-tab" 
          :class="{ active: activeCategory === category }"
          @click="activeCategory = category"
        >
          {{ category }}
        </div>
      </div>
      
      <div class="faq-section" v-for="(section, sectionIndex) in filteredFaqs" :key="sectionIndex">
        <h2>{{ section.title }}</h2>
        
        <div class="faq-item" v-for="(item, itemIndex) in section.items" :key="itemIndex">
          <div 
            class="faq-question" 
            :class="{ active: activeQuestion === `${sectionIndex}-${itemIndex}` }"
            @click="toggleQuestion(`${sectionIndex}-${itemIndex}`)"
          >
            {{ item.question }}
            <i class="fas fa-chevron-down"></i>
          </div>
          
          <div class="faq-answer" :class="{ active: activeQuestion === `${sectionIndex}-${itemIndex}` }">
            {{ item.answer }}
          </div>
        </div>
      </div>
      
      <div class="contact-section">
        <h2>还有疑问？联系我们</h2>
        
        <div class="contact-methods">
          <div class="contact-method">
            <div class="contact-icon">
              <i class="fas fa-envelope"></i>
            </div>
            <div class="contact-info">
              <h3>电子邮件</h3>
              <p>support@lingcycling.com</p>
            </div>
          </div>
          
          <div class="contact-method">
            <div class="contact-icon">
              <i class="fas fa-phone-alt"></i>
            </div>
            <div class="contact-info">
              <h3>电话</h3>
              <p>400-123-4567</p>
            </div>
          </div>
          
          <div class="contact-method">
            <div class="contact-icon">
              <i class="fas fa-comments"></i>
            </div>
            <div class="contact-info">
              <h3>在线客服</h3>
              <p>工作日 9:00-18:00</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed } from 'vue';

const searchQuery = ref('');
const activeCategory = ref('所有问题');
const activeQuestion = ref(null);

const categories = [
  '所有问题',
  '账户相关',
  '骑行路线',
  '安全指南',
  '设备保养',
  '应用功能'
];

const faqs = [
  {
    title: '账户与注册',
    category: '账户相关',
    items: [
      {
        question: '如何注册新账户？',
        answer: '点击网站右上角的"注册