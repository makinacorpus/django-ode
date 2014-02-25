# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contact'
        db.create_table(u'accounts_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['Contact'])

        # Adding model 'Organization'
        db.create_table(u'accounts_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('activity_field', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('post_code', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('town', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('is_provider', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_consumer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_host', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_creator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_performer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_media', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_website', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_mobile_app', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_other', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('media_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('website_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('mobile_app_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('other_details', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('price_information', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('audience', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('capacity', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('ticket_contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ticket_organization', null=True, to=orm['accounts.Contact'])),
            ('press_contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='press_organization', null=True, to=orm['accounts.Contact'])),
        ))
        db.send_create_signal(u'accounts', ['Organization'])

        # Adding model 'User'
        db.create_table(u'accounts_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Organization'], null=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('confirmation_code', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('first_inscription', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'accounts', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name(u'accounts_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'accounts.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name(u'accounts_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'accounts.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])


    def backwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table(u'accounts_contact')

        # Deleting model 'Organization'
        db.delete_table(u'accounts_organization')

        # Deleting model 'User'
        db.delete_table(u'accounts_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name(u'accounts_user_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name(u'accounts_user_user_permissions'))


    models = {
        u'accounts.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'accounts.organization': {
            'Meta': {'object_name': 'Organization'},
            'activity_field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'audience': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_consumer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_creator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_host': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_media': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_mobile_app': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_performer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_provider': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_website': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'media_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'mobile_app_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'other_details': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'press_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'press_organization'", 'null': 'True', 'to': u"orm['accounts.Contact']"}),
            'price_information': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'ticket_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ticket_organization'", 'null': 'True', 'to': u"orm['accounts.Contact']"}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'confirmation_code': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_inscription': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Organization']", 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']