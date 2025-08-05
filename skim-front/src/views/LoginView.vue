<template>
  <div>
    <button @click="handleGoogleLogin">구글 로그인</button>
  </div>
</template>

<script setup>
const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
const redirectUri = import.meta.env.VITE_GOOGLE_REDIRECT_URI
const scope = 'openid email profile'
const responseType = 'code'

function handleGoogleLogin() {
  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${encodeURIComponent(scope)}&access_type=offline&prompt=consent`
  window.location.href = authUrl
}
</script>
