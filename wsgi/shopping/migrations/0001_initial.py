# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HomePage'
        db.create_table(u'shopping_homepage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
        ))
        db.send_create_signal(u'shopping', ['HomePage'])

        # Adding model 'Product'
        db.create_table(u'shopping_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            (u'rating_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            (u'rating_sum', self.gf('django.db.models.fields.IntegerField')(default=0)),
            (u'rating_average', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('unit_price', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('sale_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_price', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('sale_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sale_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sku', self.gf('shopping.fields.SKUField')(max_length=20, unique=True, null=True, blank=True)),
            ('num_in_stock', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.CustomUser'])),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('review_point', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('view', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('like', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'shopping', ['Product'])

        # Adding M2M table for field categories on 'Product'
        m2m_table_name = db.shorten_name(u'shopping_product_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'shopping.product'], null=False)),
            ('category', models.ForeignKey(orm[u'shopping.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'category_id'])

        # Adding M2M table for field related_products on 'Product'
        m2m_table_name = db.shorten_name(u'shopping_product_related_products')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_product', models.ForeignKey(orm[u'shopping.product'], null=False)),
            ('to_product', models.ForeignKey(orm[u'shopping.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_product_id', 'to_product_id'])

        # Adding M2M table for field upsell_products on 'Product'
        m2m_table_name = db.shorten_name(u'shopping_product_upsell_products')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_product', models.ForeignKey(orm[u'shopping.product'], null=False)),
            ('to_product', models.ForeignKey(orm[u'shopping.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_product_id', 'to_product_id'])

        # Adding model 'ProductsPage'
        db.create_table(u'shopping_productspage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'shopping', ['ProductsPage'])

        # Adding model 'ProductImage'
        db.create_table(u'shopping_productimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('image', self.gf('mezzanine.core.fields.FileField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['shopping.Product'])),
        ))
        db.send_create_signal(u'shopping', ['ProductImage'])

        # Adding model 'ProductOption'
        db.create_table(u'shopping_productoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('shopping.fields.OptionField')(max_length=50, null=True)),
        ))
        db.send_create_signal(u'shopping', ['ProductOption'])

        # Adding model 'ProductVariation'
        db.create_table(u'shopping_productvariation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit_price', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('sale_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_price', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('sale_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sale_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sku', self.gf('shopping.fields.SKUField')(max_length=20, unique=True, null=True, blank=True)),
            ('num_in_stock', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variations', to=orm['shopping.Product'])),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shopping.ProductImage'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('option1', self.gf('shopping.fields.OptionField')(max_length=50, null=True)),
            ('option2', self.gf('shopping.fields.OptionField')(max_length=50, null=True)),
        ))
        db.send_create_signal(u'shopping', ['ProductVariation'])

        # Adding model 'Category'
        db.create_table(u'shopping_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('featured_image', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('sale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shopping.Sale'], null=True, blank=True)),
            ('price_min', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('price_max', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('combined', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'shopping', ['Category'])

        # Adding M2M table for field products on 'Category'
        m2m_table_name = db.shorten_name(u'shopping_category_products')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm[u'shopping.category'], null=False)),
            ('product', models.ForeignKey(orm[u'shopping.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['category_id', 'product_id'])

        # Adding M2M table for field options on 'Category'
        m2m_table_name = db.shorten_name(u'shopping_category_options')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm[u'shopping.category'], null=False)),
            ('productoption', models.ForeignKey(orm[u'shopping.productoption'], null=False))
        ))
        db.create_unique(m2m_table_name, ['category_id', 'productoption_id'])

        # Adding model 'Sale'
        db.create_table(u'shopping_sale', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('discount_deduct', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('discount_percent', self.gf('shopping.fields.PercentageField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('discount_exact', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('valid_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('valid_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'shopping', ['Sale'])

        # Adding M2M table for field products on 'Sale'
        m2m_table_name = db.shorten_name(u'shopping_sale_products')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sale', models.ForeignKey(orm[u'shopping.sale'], null=False)),
            ('product', models.ForeignKey(orm[u'shopping.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sale_id', 'product_id'])

        # Adding M2M table for field categories on 'Sale'
        m2m_table_name = db.shorten_name(u'shopping_sale_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sale', models.ForeignKey(orm[u'shopping.sale'], null=False)),
            ('category', models.ForeignKey(orm[u'shopping.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sale_id', 'category_id'])

        # Adding model 'DiscountCode'
        db.create_table(u'shopping_discountcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('discount_deduct', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('discount_percent', self.gf('shopping.fields.PercentageField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('discount_exact', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('valid_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('valid_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('code', self.gf('shopping.fields.DiscountCodeField')(unique=True, max_length=20)),
            ('min_purchase', self.gf('shopping.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('free_shipping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uses_remaining', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'shopping', ['DiscountCode'])

        # Adding M2M table for field products on 'DiscountCode'
        m2m_table_name = db.shorten_name(u'shopping_discountcode_products')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('discountcode', models.ForeignKey(orm[u'shopping.discountcode'], null=False)),
            ('product', models.ForeignKey(orm[u'shopping.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['discountcode_id', 'product_id'])

        # Adding M2M table for field categories on 'DiscountCode'
        m2m_table_name = db.shorten_name(u'shopping_discountcode_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('discountcode', models.ForeignKey(orm[u'shopping.discountcode'], null=False)),
            ('category', models.ForeignKey(orm[u'shopping.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['discountcode_id', 'category_id'])

        # Adding model 'ExtendForum'
        db.create_table(u'shopping_extendforum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pybb.Forum'], unique=True)),
            ('image', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'shopping', ['ExtendForum'])


    def backwards(self, orm):
        # Deleting model 'HomePage'
        db.delete_table(u'shopping_homepage')

        # Deleting model 'Product'
        db.delete_table(u'shopping_product')

        # Removing M2M table for field categories on 'Product'
        db.delete_table(db.shorten_name(u'shopping_product_categories'))

        # Removing M2M table for field related_products on 'Product'
        db.delete_table(db.shorten_name(u'shopping_product_related_products'))

        # Removing M2M table for field upsell_products on 'Product'
        db.delete_table(db.shorten_name(u'shopping_product_upsell_products'))

        # Deleting model 'ProductsPage'
        db.delete_table(u'shopping_productspage')

        # Deleting model 'ProductImage'
        db.delete_table(u'shopping_productimage')

        # Deleting model 'ProductOption'
        db.delete_table(u'shopping_productoption')

        # Deleting model 'ProductVariation'
        db.delete_table(u'shopping_productvariation')

        # Deleting model 'Category'
        db.delete_table(u'shopping_category')

        # Removing M2M table for field products on 'Category'
        db.delete_table(db.shorten_name(u'shopping_category_products'))

        # Removing M2M table for field options on 'Category'
        db.delete_table(db.shorten_name(u'shopping_category_options'))

        # Deleting model 'Sale'
        db.delete_table(u'shopping_sale')

        # Removing M2M table for field products on 'Sale'
        db.delete_table(db.shorten_name(u'shopping_sale_products'))

        # Removing M2M table for field categories on 'Sale'
        db.delete_table(db.shorten_name(u'shopping_sale_categories'))

        # Deleting model 'DiscountCode'
        db.delete_table(u'shopping_discountcode')

        # Removing M2M table for field products on 'DiscountCode'
        db.delete_table(db.shorten_name(u'shopping_discountcode_products'))

        # Removing M2M table for field categories on 'DiscountCode'
        db.delete_table(db.shorten_name(u'shopping_discountcode_categories'))

        # Deleting model 'ExtendForum'
        db.delete_table(u'shopping_extendforum')


    models = {
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
        },
        u'pages.page': {
            'Meta': {'ordering': "(u'titles',)", 'object_name': 'Page'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_menus': ('mezzanine.pages.fields.MenusField', [], {'default': '(1, 2)', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['pages.Page']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'profiles.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'pybb.category': {
            'Meta': {'ordering': "[u'position']", 'object_name': 'Category'},
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'pybb.forum': {
            'Meta': {'ordering': "[u'position']", 'object_name': 'Forum'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'forums'", 'to': u"orm['pybb.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'headline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['profiles.CustomUser']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'child_forums'", 'null': 'True', 'to': u"orm['pybb.Forum']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'readed_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'readed_forums'", 'symmetrical': 'False', 'through': u"orm['pybb.ForumReadTracker']", 'to': u"orm['profiles.CustomUser']"}),
            'topic_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pybb.forumreadtracker': {
            'Meta': {'unique_together': "((u'user', u'forum'),)", 'object_name': 'ForumReadTracker'},
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pybb.Forum']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.CustomUser']"})
        },
        u'shopping.category': {
            'Meta': {'object_name': 'Category'},
            'combined': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'featured_image': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'product_options'", 'blank': 'True', 'to': u"orm['shopping.ProductOption']"}),
            'price_max': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'price_min': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['shopping.Product']", 'symmetrical': 'False', 'blank': 'True'}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shopping.Sale']", 'null': 'True', 'blank': 'True'})
        },
        u'shopping.discountcode': {
            'Meta': {'object_name': 'DiscountCode'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'discountcode_related'", 'blank': 'True', 'to': u"orm['shopping.Category']"}),
            'code': ('shopping.fields.DiscountCodeField', [], {'unique': 'True', 'max_length': '20'}),
            'discount_deduct': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'discount_exact': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'discount_percent': ('shopping.fields.PercentageField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_purchase': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['shopping.Product']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uses_remaining': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'valid_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'shopping.extendforum': {
            'Meta': {'object_name': 'ExtendForum'},
            'forum': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pybb.Forum']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'shopping.homepage': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'HomePage', '_ormbases': [u'pages.Page']},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'shopping.product': {
            'Meta': {'object_name': 'Product'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['shopping.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'num_in_stock': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'related_products': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_products_rel_+'", 'blank': 'True', 'to': u"orm['shopping.Product']"}),
            'review_point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sale_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sale_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_price': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'sale_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'sku': ('shopping.fields.SKUField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'unit_price': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'upsell_products': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'upsell_products_rel_+'", 'blank': 'True', 'to': u"orm['shopping.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.CustomUser']"}),
            'view': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'shopping.productimage': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ProductImage'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('mezzanine.core.fields.FileField', [], {'max_length': '255'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['shopping.Product']"})
        },
        u'shopping.productoption': {
            'Meta': {'object_name': 'ProductOption'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('shopping.fields.OptionField', [], {'max_length': '50', 'null': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'shopping.productspage': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ProductsPage', '_ormbases': [u'pages.Page']},
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'shopping.productvariation': {
            'Meta': {'ordering': "('-default',)", 'object_name': 'ProductVariation'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shopping.ProductImage']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'num_in_stock': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'option1': ('shopping.fields.OptionField', [], {'max_length': '50', 'null': 'True'}),
            'option2': ('shopping.fields.OptionField', [], {'max_length': '50', 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variations'", 'to': u"orm['shopping.Product']"}),
            'sale_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sale_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_price': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'sale_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sku': ('shopping.fields.SKUField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'unit_price': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        u'shopping.sale': {
            'Meta': {'object_name': 'Sale'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'sale_related'", 'blank': 'True', 'to': u"orm['shopping.Category']"}),
            'discount_deduct': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'discount_exact': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'discount_percent': ('shopping.fields.PercentageField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['shopping.Product']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'valid_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['shopping']