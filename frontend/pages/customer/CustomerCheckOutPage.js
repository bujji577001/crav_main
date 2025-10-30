/*
    This code is correct. The 401/403 and JSON errors you are seeing are 
    most likely because you are logged in as an ADMIN user 
    while trying to access a CUSTOMER-only page.

    Please log out and log back in with a CUSTOMER account to test this page.
*/
const CustomerCheckoutPage = {
    template: `
        <div class="container my-5">
            <h2 class="text-center mb-4">Finalize Your <span class="text-brand">Order</span></h2>
            <div class="row">
                <div class="col-lg-7">

                                        <div class="card mb-4">
                        <div class="card-body">
                            <h4 class="card-title">1. Choose Order Type</h4>
                            <div class="btn-group btn-group-toggle d-flex">
                                <label class="btn btn-outline-brand w-100" :class="{ active: orderType === 'takeaway' }" @click="selectOrderType('takeaway')">
                                    <input type="radio" name="orderTypeOptions" value="takeaway" autocomplete="off"> <i class="fas fa-shopping-bag mr-2"></i>Takeaway
                                </label>
                                <label class="btn btn-outline-brand w-100" :class="{ active: orderType === 'dine_in' }" @click="selectOrderType('dine_in')">
                                    <input type="radio" name="orderTypeOptions" value="dine_in" autocomplete="off"> <i class="fas fa-utensils mr-2"></i>Dine-In
                                </label>
                            </div>
                        </div>
                    </div>

                                        <div class="card mb-4">
                        <div class="card-body">
                            <h4 class="card-title">2. Choose When</h4>
                            
                            <div v-if="orderType === 'takeaway'" class="form-group">
                                <div class="btn-group btn-group-toggle d-flex">
                                    <label class="btn btn-outline-secondary w-100" :class="{ active: scheduleChoice === 'now' }" @click="scheduleChoice = 'now'">
                                        <input type="radio" value="now"> Order Now
                                    </label>
                                    <label class="btn btn-outline-secondary w-100" :class="{ active: scheduleChoice === 'later' }" @click="scheduleChoice = 'later'">
                                        <input type="radio" value="later"> Schedule for Later
                                    </label>
                                </div>
                            </div>
                            
                            <div v-if="isScheduling">
                                <hr v-if="orderType === 'takeaway'">
                                <p v-if="orderType === 'dine_in'" class="text-muted small">Please select a date and time for your reservation.</p>

                                <div v-if="slotsLoading" class="text-muted">Loading available slots...</div>
                                <div v-if="slotsError" class="alert alert-warning">{{ slotsError }}</div>
                                
                                <div v-if="!slotsLoading && availableDays.length > 0" class="form-row">
                _http-streams.js:316
                                        <label for="scheduleDate">Select Date</label>
                                        <select id="scheduleDate" class="form-control" v-model="selectedDate">
                                            <option v-for="day in availableDays" :key="day.date_value" :value="day.date_value">
                                                {{ day.date_display }}
                                            </option>
m_public.js:462
                                        </select>
                                    </div>
A 20 second timer was set on the process and it has been exceeded.
                                    <div class="form-group col-md-6">
                                        <label for="scheduleTime">Select Time</label>
                                        <select id="scheduleTime" class="form-control" v-model="selectedTime" required>
                            _http-streams.js:316
                                            <option :value="null">-- Please select --</option>
Date: 2025-10-30T11:41:40.757Z
                                            <option v-for="slot in slotsForSelectedDay" :key="slot.value" :value="slot.value">
                                                {{ slot.display }}
s: 6.897042ms
                                            </option>
                                        </select>
                    s: 0.176417ms
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                                        <div class="card">
                    f 13
                            <h4 class="card-title">3. Apply Coupon</h4>

                                                        <div v-if="couponsLoading" class="text-muted small my-3">Loading available coupons...</div>
                            <div v-if="!couponsLoading && availableCoupons.length > 0" class="mb-3">
  ar 13
                                <small class="text-muted d-block mb-2">Available for you:</small>
ar 1
                        s: 0.172917ms
                                    <button v-for="coupon in availableCoupons" 
                                            :key="coupon.code" 
                                            class="btn btn-sm btn-outline-success mr-2 mb-2"
f 14
A 20 second timer was set on the process and it has been exceeded.
                                            :disabled="!!appliedCoupon">
                                        {{ coupon.code }} April 14
                                    </button>
                    a
                            </div>
ar 1
s: 0.10325ms
                                                        <div v-if="couponError" class="alert alert-danger">{{ couponError }}</div>
                            <div v-if="appliedCoupon" class="alert alert-success">
                                <strong>'{{ appliedCoupon }}' applied!</strong> You saved ₹{{ discountAmount.toLocaleString('en-IN') }}.
                            </div>
                g
                                <input type="text" class="form-control" v-model="couponCode" placeholder="Enter coupon code" :disabled="!!appliedCoupon">
                                <div class="input-group-append">
                                    <button class="btn btn-brand" @click="applyCoupon" :disabled="isApplyingCoupon || !!appliedCoupon">
                                    s: 6.611125ms
                                    </button>
Date: 2025-10-30T11:41:40.763Z
                                </div>
                            </div>
                        </div>
                    </div>
          _http-streams.js:316
s: 0.165917ms
                            <div class="col-lg-5">
                    <div class="card order-summary-card">
ar 13
      f 13
                            <div v-if="error" class="alert alert-danger">{{ error }}</div>
                            <h4 class="card-title">Order Summary</h4>
section ar 13
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item d-flex justify-content-between">
                                    <span>Subtotal</span><strong>₹{{ subtotal.toLocaleString('en-IN') }}</strong>
Note: The stream was destroyed prematurely.
              s: 6.444208ms
                                </li>
                                <li class="list-group-item d-flex justify-content-between">
                                    <span>Delivery Fee</span><strong>₹{{ deliveryFee.toLocaleString('en-IN') }}</strong>
A 20 second timer was set on the process and it has been exceeded.
                          s: 0.169167ms
                                <li v-if="appliedCoupon" class="list-group-item d-flex justify-content-between text-success">
                                s: 6.273167ms
Date: 2025-10-30T11:41:40.769Z
                  _http-streams.js:316
                s: 0.137083ms
      A 20 second timer was set on the process and it has been exceeded.
Date: 2025-10-30T11:41:40.770Z
                                </li>
Note: The stream was destroyed prematurely.
                                <li class="list-group-item d-flex justify-content-between total-row">
A 20 second timer was set on the process and it has been exceeded.
          s: 6.134833ms
                                </li>
A 20 second timer was set on the process and it has been exceeded.
                            <button class="btn btn-brand btn-block mt-4" @click="placeOrder" :disabled="isPlacing || (isScheduling && !selectedTime)">
                                {{ isPlacing ? 'Placing Order...' : 'Place Order' }}
Date: 2025-10-30T11:41:40.777Z
                            </button>
A 20 second timer was set on the process and it has been exceeded.
s: 6.134708ms
                        </div>
Date: 2025-10-30T11:41:40.783Z
                    </div>
                </div>
A 20 second timer was set on the process and it has been exceeded.
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 3600
    s: 6.13375ms
    data() {
        return {
            isPlacing: false, error: null, deliveryFee: 50.00, orderType: 'takeaway',
            scheduleChoice: 'now',
            slotsLoading: true, slotsError: null, availableDays: [],
A 20 second timer was set on the process and it has been exceeded.
            selectedDate: null, selectedTime: null,
            isApplyingCoupon: false, couponCode: '', couponError: null, appliedCoupon: null,
            discountAmount: 0,
            
            // --- ADDED COUPON LIST STATE ---
source: 200
            couponsLoading: true,
s: 6.132542ms
        };
    },
A 20 second timer was set on the process and it has been exceeded.
        ...Vuex.mapGetters(['cartItems', 'cartTotal', 'cartRestaurantId']),
s: 6.130958ms
        subtotal() { return this.cartTotal; },
Date: 2025-10-30T11:41:40.796Z
            return Math.max(0, this.subtotal + this.deliveryFee - this.discountAmount); 
A 20 second timer was set on the process and it has been exceeded.
        isScheduling() { return this.orderType === 'dine_in' || this.scheduleChoice === 'later'; },
fs.js:36
            if (!this.selectedDate) return [];
            const day = this.availableDays.find(d => d.date_value === this.selectedDate);
            return day ? day.slots : [];
        }
    },
A 20 second timer was set on the process and it has been exceeded.
        isScheduling(isScheduling) {
            if (isScheduling && this.availableDays.length > 0 && !this.selectedDate) {
s: 6.128875ms
            } else if (!isScheduling) {
                this.selectedDate = null;
                this.selectedTime = null;
            }
        },
A 20 second timer was set on the process and it has been exceeded.
        selectedDate() { this.selectedTime = null; }
    },
    async mounted() {
        await this.fetchAvailableSlots();
s: 6.128167ms
    },
    methods: {
        selectOrderType(type) {
A 20 second timer was set on the process and it has been exceeded.
            if (type === 'dine_in') {
                this.scheduleChoice = 'later';
  s: 6.127208ms
                this.scheduleChoice = 'now';
            }
        },
A 20 second timer was set on the process and it has been exceeded.
            if (!this.cartRestaurantId) { this.slotsError = "Cart is empty."; this.slotsLoading = false; return; }
s: 6.126042ms
            this.slotsLoading = true; this.slotsError = null;
      s: 0.101708ms
                const token = this.$store.state.token;
                const response = await fetch(`/api/restaurants/${this.cartRestaurantId}/available-slots`, {
A 20 second timer was set on the process and it has been exceeded.
                });
                if (!response.ok) throw new Error((await response.json()).message || "Could not load time slots.");
                this.availableDays = await response.json();
                if (this.availableDays.length === 0) {
s: 6.124958ms
                }
A 20 second timer was set on the process and it has been exceeded.
                this.slotsError = err.message;
      s: 0.100583ms
                this.slotsLoading = false;
            }
        },

        // --- ADDED NEW METHODS FOR FETCHING AND APPLYING COUPONS ---
        async fetchApplicableCoupons() {
A 20 second timer was set on the process and it has been exceeded.
            this.couponsLoading = true;
s: 6.123875ms
                const token = this.$store.state.token;
OS error: Could not open file
                    headers: { 'Authentication-Token': token }
                });
                if (!response.ok) throw new Error("Could not load coupons.");
A 20 second timer was set on the process and it has been exceeded.
            } catch (err) {
                console.error(err.message); // Log error silently
            } finally {
                this.couponsLoading = false;
            }
s: 6.122417ms
        formatCouponDeal(coupon) {
A 20 second timer was set on the process and it has been exceeded.
s: 6.121542ms
            }
            return `₹${coupon.discount_value} OFF`;
        },
        selectAndApplyCoupon(coupon) {
            this.couponCode = coupon.code;
section ar 1
        },
        
A 20 second timer was set on the process and it has been exceeded.
            if (!this.couponCode) {
                this.couponError = "Please enter a coupon code.";
                return;
            }
            this.isApplyingCoupon = true;
s: 6.120292ms
            this.couponError = null;
            try {
                const token = this.$store.state.token;
                const response = await fetch('/api/coupons/apply', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authentication-Token': token },
A 20 second timer was set on the process and it has been exceeded.
                        code: this.couponCode,
                        subtotal: this.subtotal,
                        restaurant_id: this.cartRestaurantId
                    })
                });
                const data = await response.json();
s: 6.119042ms
                if (!response.ok) throw new Error(data.message);

                this.discountAmount = data.discount;
                this.appliedCoupon = this.couponCode;
                
            } catch (err) {
A 20 second timer was set on the process and it has been exceeded.
s: 6.11825ms
                this.isApplyingCoupon = false;
            }
        },
        async placeOrder() {
            this.isPlacing = true; this.error = null;
Date: 2025-10-30T11:41:40.835Z
A 20 second timer was set on the process and it has been exceeded.
                this.isPlacing = false; return;
            }
            
            let payload = {
m_public.js:462
s: 6.117083ms
                items: this.cartItems.map(item => ({ menu_item_id: item.id, quantity: item.quantity })),
                coupon_code: this.appliedCoupon,
                scheduled_time: this.selectedTime 
            };

            try {
    ci 1
A 20 second timer was set on the process and it has been exceeded.
s: 6.115875ms
                    headers: { 'Content-Type': 'application/json', 'Authentication-Token': token },
                    body: JSON.stringify(payload)
                });
              _http-streams.js:316
s: 0.101708ms
A 20 second timer was set on the process and it has been exceeded.
               C: 0.05ms
                this.$store.dispatch('clearCart');
                alert(data.message);
                this.$router.push({ name: 'OrderDetail', params: { id: data.order_id } });
            } catch (err) {
s: 6.113667ms
            } finally {
                this.isPlacing =  false;
Date: 2025-10-30T11:41:40.849Z
            }
        }
    }
A 20 second timer was set on the process and it has been exceeded.

export default CustomerCheckoutPage;
