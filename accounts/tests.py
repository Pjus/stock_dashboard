from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser


class AccountsAPITestCase(TestCase):
    def setUp(self):
        # API 클라이언트를 초기화하고 기본 사용자 데이터를 생성합니다.
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strong_password123',
            'password2': 'strong_password123',
            'phone_number': '01012345678',
            'date_of_birth': '2000-01-01'
        }
        # 기존 사용자 생성
        self.user = CustomUser.objects.create_user(
            username='existinguser',
            email='existinguser@example.com',
            password='password123'
        )

    def test_register_user(self):
        # 회원가입 테스트
        response = self.client.post('/api/accounts/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  # 기존 사용자 + 새 사용자
        self.assertEqual(CustomUser.objects.get(
            username='testuser').email, 'testuser@example.com')

    def test_register_user_password_mismatch(self):
        # 비밀번호 불일치 테스트
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'wrong_password'
        response = self.client.post('/api/accounts/register/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login_user(self):
        # 로그인 테스트
        login_data = {'username': 'existinguser', 'password': 'password123'}
        response = self.client.post('/api/accounts/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        # 잘못된 로그인 테스트
        login_data = {'username': 'existinguser', 'password': 'wrong_password'}
        response = self.client.post('/api/accounts/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail(self):
        # 사용자 상세 정보 조회 테스트
        login_data = {'username': 'existinguser', 'password': 'password123'}
        login_response = self.client.post('/api/accounts/login/', login_data)
        access_token = login_response.data['access']

        # 인증 헤더에 토큰 추가
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/accounts/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')
        self.assertEqual(response.data['email'], 'existinguser@example.com')

    def test_unauthorized_user_detail(self):
        # 인증되지 않은 사용자 요청 테스트
        response = self.client.get('/api/accounts/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordResetTestCase(TestCase):
    def setUp(self):
        # 테스트 클라이언트 초기화
        self.client = APIClient()
        # 테스트 사용자 생성
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.reset_request_url = '/api/accounts/password-reset/'
        self.reset_confirm_url = '/api/accounts/password-reset-confirm/'

    def test_password_reset_request(self):
        """비밀번호 재설정 요청 테스트"""
        response = self.client.post(self.reset_request_url, {
                                    'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         "Password reset email sent.")

    def test_password_reset_request_invalid_email(self):
        """존재하지 않는 이메일로 비밀번호 재설정 요청"""
        response = self.client.post(self.reset_request_url, {
                                    'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_password_reset_confirm_valid_token(self):
        """유효한 토큰으로 비밀번호 재설정"""
        # 토큰 생성
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = PasswordResetTokenGenerator().make_token(self.user)
        new_password = 'newpassword123'

        # 새 비밀번호 설정 요청
        response = self.client.post(self.reset_confirm_url, {
            'uid': uid,
            'token': token,
            'new_password': new_password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         "Password has been reset successfully.")

        # 새 비밀번호로 로그인 확인
        self.user.refresh_from_db()
        login_successful = self.user.check_password(new_password)
        self.assertTrue(login_successful)

    def test_password_reset_confirm_invalid_token(self):
        """잘못된 토큰으로 비밀번호 재설정 시도"""
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        invalid_token = 'invalid-token'
        new_password = 'newpassword123'

        response = self.client.post(self.reset_confirm_url, {
            'uid': uid,
            'token': invalid_token,
            'new_password': new_password
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)  # 수정
        self.assertIn('Invalid or expired token.',
                      response.data['non_field_errors'])  # 추가

    def test_password_reset_confirm_invalid_uid(self):
        """잘못된 UID로 비밀번호 재설정 시도"""
        invalid_uid = urlsafe_base64_encode(
            force_bytes(99999))  # 존재하지 않는 사용자 ID
        token = PasswordResetTokenGenerator().make_token(self.user)
        new_password = 'newpassword123'

        response = self.client.post(self.reset_confirm_url, {
            'uid': invalid_uid,
            'token': token,
            'new_password': new_password
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)  # 수정
        self.assertIn('Invalid user ID.',
                      response.data['non_field_errors'])  # 추가
