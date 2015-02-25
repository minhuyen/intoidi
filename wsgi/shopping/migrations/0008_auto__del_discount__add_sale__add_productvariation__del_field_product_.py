# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Discount'
        db.delete_table(u'shopping_discount')

        # Removing M2M table for field products on 'Discount'
        db.delete_table(db.shorten_name(u'shopping_discount_products'))

        # Removing M2M table for field categories on 'Discount'
        db.delete_table(db.shorten_name(u'shopping_discount_categories'))

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

        # Deleting field 'Product.product_code'
        db.delete_column(u'shopping_product', 'product_code')

        # Adding field 'Product.manufacturer'
        db.add_column(u'shopping_product', 'manufacturer',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Discount'
        db.create_table(u'shopping_discount', (
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('discount_exact', self.gf('django.db.models.fields.FloatField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('discount_deduct', self.gf('django.db.models.fields.FloatField')()),
            ('valid_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('valid_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('discount_percent', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'shopping', ['Discount'])

        # Adding M2M table for field products on 'Discount'
        m2m_table_name = db.shorten_name(u'shopping_discount_products')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('discount', models.ForeignKey(orm[u'shopping.discount'], null=False)),
            ('product', models.ForeignKey(orm[u'shopping.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['discount_id', 'product_id'])

        # Adding M2M table for field categories on 'Discount'
        m2m_table_name = db.shorten_name(u'shopping_discount_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('discount', models.ForeignKey(orm[u'shopping.discount'], null=False)),
            ('category', models.ForeignKey(orm[u'shopping.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['discount_id', 'category_id'])

        # Deleting model 'Sale'
        db.delete_table(u'shopping_sale')

        # Removing M2M table for field products on 'Sale'
        db.delete_table(db.shorten_name(u'shopping_sale_products'))

        # Removing M2M table for field categories on 'Sale'
        db.delete_table(db.shorten_name(u'shopping_sale_categories'))

        # Deleting model 'ProductVariation'
        db.delete_table(u'shopping_productvariation')

        # Adding field 'Product.product_code'
        db.add_column(u'shopping_product', 'product_code',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Product.manufacturer'
        db.delete_column(u'shopping_product', 'manufacturer')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
        u'shopping.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'product_options'", 'blank': 'True', 'to': u"orm['shopping.ProductOption']"}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['shopping.Product']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'shopping.homepage': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'HomePage', '_ormbases': [u'pages.Page']},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'shopping.product': {
            'Meta': {'object_name': 'Product'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_in_stock': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'review_point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sale_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sale_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_price': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'sale_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sku': ('shopping.fields.SKUField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'unit_price': ('shopping.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
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