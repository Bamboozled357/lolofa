from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from rest_framework import serializers


User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)
    name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=False)
    """метод validate_имя_поля служит для того, чтобы проверить одно конкретное поле"""
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Почта уже занята')
        return email
    """один общий метод validate осуществляет проверку всех имеющихся полей. при этом, 
    возвращает поля он в виде словарей, где названия являются их ключами, а attrs - значениями"""
    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs


    def create(self, attrs): #attrs может называться и как validated_data
        user = User.objects.create_user(**attrs)
        user.create_activation_code() # после того как во въюхах создали код активации:
        user.send_activation_mail()# отправляем пользователю письмо подтверждения
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=8, max_length=8, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Код недействителен')
        return code

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email=email,
                                   activation_code=code).exists():
            raise serializers.ValidationError('Данные не совпадают')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()

"""при входе вам выдаётся ключ(токен), который вы будете передавать на сервер"""
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6)
    """проверяем в методе существует ли такой пользователь"""
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    """метод в котором получаем request из вьюшки, далее идут проверки на заполнение почты и пароля
если что-то не так, сгенерировать ошибки. Если всё норм, то под ключом user вернуть attrs"""
    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email', 'password')
        password = attrs.get('password')
        if email and password:
            user = authenticate(username=email,
                                password=password,
                                request=request)
            if not user:
                raise serializers.ValidationError('Неверный email или пароль')
        else:
            raise serializers.ValidationError('Email и пароль обязательны для заполнения')
        attrs['user'] = user
        return attrs



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Неверный пароль')
        return old_password

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()


# 1. вариант где при восстановлении пароля мы САМИ выдадим новый пароль, который при желании юзер, может сменить после
# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#
#     def validate_email(self, email):
#         if not User.objects.filter(email=email).exists():
#             """если юзера с такой почтой не было, то нечего восстанавливать такого пользователя никогда не было"""
#             raise serializers.ValidationError('Пользователь не зарегистрирован')
#         return email
#
#     def send_new_password(self):
#         email = self.validated_data.get('email')
#         user = User.objects.get(email=email)
#         password = User.objects.make_random_password()
#         user.set_password(password)
#         user.save()
#         send_mail('Восстановление пароля',
#                   f'Ваш новый пароль: {password}',
#                   'test@test.com',
#                   [email])

# 2. вариант где при восстановлении отправляем юзеру код подтверждения, а он сам создаёт новый пароль
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            """если юзера с такой почтой не было, то нечего восстанавливать такого пользователя никогда не было"""
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'Восстановление пароля',
            f'Ваш код подтверждения: {user.activation_code}',
            'test@test.com',
            [email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=8, max_length=8, required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()
