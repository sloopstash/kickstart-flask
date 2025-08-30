/*!
 * Main functionalities.
 */

// Define global namespace.
var app = app || {};

// Allow other libraries to use $.
// jQuery.noConflict();

// Initialize JQuery.
(function($) {
  
  // Pager controller.
  app.pager = function(params) {
    this.name = params['name'];
    this.mode = params['mode'];
    this.entity = params['entity'];
    this.url = params['url'];
    this.query = params['query'];
    this.container = params['container'];
    this.content = this.container+' .block-content';
    switch(this.mode) {
      case 'normal':
        this.action = this.container+' .block-footer .block-action';
        this.previous = this.container+' .block-footer .block-action .pager .previous';
        this.next = this.container+' .block-footer .block-action .pager .next';
        break;
      default:
        break;
    }
    this.pages = 0;
    this.items = [];
    this.counter = {};
    this.execute();
  }
  app.pager.prototype.execute = function() {
    this.loader();
    this.size();
    if(this.pages!=0) {
      this.counter['current'] = 1;
      this.fetch(this.counter['current']);
      switch(this.mode) {
        case 'normal':
          this.counter['previous'] = this.counter['current']-1;
          this.counter['next'] = this.counter['current']+1;
          break;
        default:
          break;
      }
      this.render();
      this.widget();
    } else {
      this.empty();
    }
  }
  app.pager.prototype.widget = function() {
    var _this = this;
    switch(this.mode) {
      case 'normal':
        var markup = `
          <div class="pager">
          <a class="previous btn-small grey lighten-3 grey-text text-darken-3 z-depth-0 disabled">
          <i class="fa-solid fa-caret-left"></i>
          </a>
          <a class="next btn-small grey lighten-3 grey-text text-darken-3 z-depth-0">
          <i class="fa-solid fa-caret-right"></i>
          <a>
          </div>
        `;
        $(this.action).empty();
        $(this.action).append(markup);
        $(this.previous).on('click',function() {
          if(_this.counter['previous']!=0) {
            _this.loader();
            _this.fetch(_this.counter['previous']);
            _this.counter['current'] = _this.counter['current']-1;
            _this.counter['previous'] = _this.counter['previous']-1;
            _this.counter['next'] = _this.counter['next']-1;
            _this.render();
          }
          if(_this.counter['previous']==0) {
            $(_this.previous).last().addClass('disabled');
          }
          if(_this.counter['next']<=_this.pages) {
            $(_this.next).removeClass('disabled');
          }
        });
        $(this.next).on('click',function() {
          if(_this.counter['next']<=_this.pages) {
            _this.loader();
            _this.fetch(_this.counter['next']);
            _this.counter['current'] = _this.counter['current']+1;
            _this.counter['previous'] = _this.counter['previous']+1;
            _this.counter['next'] = _this.counter['next']+1;
            _this.render();
          }
          if(_this.counter['next']>_this.pages) {
            $(_this.next).last().addClass('disabled');
          }
          if(_this.counter['previous']!=0) {
            $(_this.previous).removeClass('disabled');
          }
        });
        break;
      default:
        break;
    }
  }
  app.pager.prototype.loader = function() {
    var markup = `
      <div class="progress">
      <div class="indeterminate"></div>
      </div>
    `;
    $(this.content).empty();
    $(this.content).append(markup);
  }
  app.pager.prototype.error = function() {
    var markup = `<p class="flow-text center">Error loading data.</p>`;
    $(this.content).empty();
    $(this.content).append(markup);
  }
  app.pager.prototype.empty = function() {
    var markup = `<p class="flow-text center">Not available.</p>`;
    $(this.content).empty();
    $(this.content).append(markup);
  }
  app.pager.prototype.size = function() {
    var output = null;
    $.ajax({
      url:(this.query!==null) ? this.url+'?'+this.query:this.url,
      data:{count:true},
      type:'GET',
      dataType:'json',
      async:false,
      timeout:10000,
      crossDomain:false
    }).done(function(data,status,request) {
      output = data;
    });
    if(output!==null) {
      switch(output['status']) {
        case 'success':
          this.pages = output['result']['pages'];
          break;
        case 'failure':
          this.pages = 0;
          break;
        default:
          break;
      }
    } else {
      this.error();
    }
  }
  app.pager.prototype.fetch = function(page) {
    var output = null;
    $.ajax({
      url:(this.query!==null) ? this.url+'?'+this.query:this.url,
      data:{page:page},
      type:'GET',
      dataType:'json',
      async:false,
      timeout:10000,
      crossDomain:false
    }).done(function(data,status,request) {
      output = data;
      console.log('Fetched contacts:', output);  // Log the fetched contacts
    });
    if(output!==null) {
      switch(output['status']) {
        case 'success':
          this.items = output['result']['items'];
          break;
        case 'failure':
          this.items = [];
          break;
        default:
          break;
      }
    } else {
      this.error();
    }
  }
  app.pager.prototype.render = function() {
    if(this.items.length!=0) {
      this.template();
    } else {
      this.empty();
    }
  }
  app.pager.prototype.template = function() {
    switch(this.mode) {
      case 'normal':
        var table = $('<table class="responsive-table highlight"></table>');
        var thead = $('<thead></thead>');
        var tbody = $('<tbody></tbody>');
        table.append(thead);
        table.append(tbody);
        switch(this.entity) {
          case 'customer':
            var thead_row = `
              <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Website</th>
              <th>Manage</th>
              </tr>
            `;
            thead.append(thead_row);
            $.each(this.items,function(index,item) {
              var tbody_row = `
              
                <tr>
                <td>
                <p><a href="/customer/`+item['id']+`/dashboard">`+item['name']+`</a></p>
                <p class="paragraph">`+item['description']+`</p>
                </td>
                <td>`+item['email']+`</td>
                <td>`+item['phone']+`</td>
                <td><a href="`+item['website']+`" target="_blank">`+item['website']+`</a></td>
                <td>
                <a href="/customer/`+item['id']+`/update">
                <i class="fa-solid fa-pen-clip icon"></i>
                </a>
                <a href="javascript:void(0);" class="delete-customer" data-id="`+item['id']+`">
                <i class="fa-solid fa-trash-can icon"></i>
                </a>
                </td>
                </tr>
              `;
              tbody.append(tbody_row);
            });
            break;

            case 'contact':
            var thead_row = `
              <tr>
              <th>FirstName</th>
              <th>LastName</th>
              <th>Email</th>
              <th>Phonenumber</th>
              <th>Actions</th>
              </tr>
            `;
            thead.append(thead_row);
            console.log(this.items);  // Log the fetched contact data
            $.each(this.items,function(index,item) {
              var tbody_row = `
                <tr>
                <td>
                <p><a href="/customer/`+item['customer_id']+`/dashboard">`+item['firstname']+ ' ' +item['lastname']+`</a></p>
                <p class="paragraph">`+item['description']+`</p>
                </td>
                <td>`+item['email']+`</td>
                <td>`+item['phonenumber']+`</td>
                <td>
                <a href="/customer/`+item['customer_id']+`/contact/`+item['contact_id']+`/update">
                <i class="fa-solid fa-pen-clip icon"></i>
                </a>
                </td>
                </tr>
              `;
              tbody.append(tbody_row);
            });
            break;

          default:
            break;
        }
        $(this.content).empty();
        $(this.content).append(table);
        break;
      default:
        break;
    }
  }

  // Tab controller.
  app.tab = function(params) {
    this.container = params['container'];
    this.default = params['default'];
    this.items = params['items'];
    this.execute();
  }
  app.tab.prototype.execute = function() {
    this.widget();
  }
  app.tab.prototype.widget = function() {
    var _this = this;
    var query = new URLSearchParams(window.location.search);
    var tab_item = query.get('tab');
    var _tab_item = this.container+' .tab-item';
    if(tab_item!==null) {
      this.default = tab_item;
    }
    $.each(this.items,function(index,item) {
      var identifier = item['identifier'].replace('#','');
      var tab_link = _tab_item+' .tab-link[href="#'+identifier+'"]';
      $(tab_link).on('click',function(event) {
        event.preventDefault();
        $(_tab_item).removeClass('tab-active');
        $(this).parent().addClass('tab-active');
        _this.render(item);
      });
      if(_this.default==identifier) {
        $(tab_link).trigger('click');
      }
    });
  }
  app.tab.prototype.render = function(item) {
    var content = item['identifier']+'.tab-content';
    $('.tab-content').hide();
    $(content).fadeIn('slow');
    if(item['pager']!==undefined) {
      var pager = new app.pager(item['pager']);
    }
  }
})(jQuery);
