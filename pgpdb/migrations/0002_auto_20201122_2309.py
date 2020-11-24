# Generated by Django 2.2 on 2020-11-22 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pgpdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pgppublickeymodel',
            name='algorithm',
            field=models.IntegerField(choices=[(0, 'Unknown'), (1, 'RSA (Encrypt or Sign)'), (2, 'RSA Encrypt-Only'), (3, 'RSA Sign-Only'), (16, 'Elgamal (Encrypt-Only)'), (17, 'DSA (Digital Signature Algorithm)'), (18, 'ECDH public key algorithm'), (19, 'ECDSA public key algorithm'), (20, 'formerly Elgamal Encrypt or Sign'), (21, 'Diffie-Hellman'), (22, 'EdDSA Edwards-curve Digital Signature Algorithm')], default=0),
        ),
        migrations.AlterField(
            model_name='pgpsignaturemodel',
            name='pka',
            field=models.IntegerField(choices=[(0, 'Unknown'), (1, 'RSA (Encrypt or Sign)'), (2, 'RSA Encrypt-Only'), (3, 'RSA Sign-Only'), (16, 'Elgamal (Encrypt-Only)'), (17, 'DSA (Digital Signature Algorithm)'), (18, 'ECDH public key algorithm'), (19, 'ECDSA public key algorithm'), (20, 'formerly Elgamal Encrypt or Sign'), (21, 'Diffie-Hellman'), (22, 'EdDSA Edwards-curve Digital Signature Algorithm')], default=0),
        ),
        migrations.AlterField(
            model_name='pgpuseridmodel',
            name='key',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userids', to='pgpdb.PGPKeyModel'),
        ),
    ]