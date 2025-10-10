#!/usr/bin/env python3
"""
Instagram Playwright Unfollow Bot - Versión mejorada con soporte para múltiples navegadores
"""
import asyncio
import json
import time
import random
import sys
import os
from playwright.async_api import async_playwright, Page, Browser

async def check_playwright_installation():
    """Check if Playwright and browsers are properly installed"""
    try:
        print("🔍 Checking Playwright installation...")
        
        # Test basic import
        from playwright.async_api import async_playwright
        print("✅ Playwright module imported successfully")
        
        # Test if chromium is available
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=True)
        await browser.close()
        await pw.stop()
        print("✅ Chromium browser is available")
        
        return True
        
    except ImportError:
        print("❌ Playwright is not installed")
        print("🔧 Please run: pip install playwright")
        return False
    except Exception as e:
        if "browser is not installed" in str(e).lower() or "executable doesn't exist" in str(e).lower():
            print("❌ Playwright browsers are not installed")
            print("🔧 Please run: playwright install chromium")
            return False
        else:
            print(f"❌ Playwright test failed: {e}")
            return False

class InstagramPlaywrightBot:
    def __init__(self, username: str, password: str, headless: bool = False, browser_type: str = "firefox"):
        self.username = username
        self.password = password
        self.headless = headless
        self.browser_type = browser_type
        self.trusted_accounts = self.load_trusted_accounts()
        self.page = None
        self.browser = None
        self.context = None
        self.playwright = None
        
    def load_trusted_accounts(self):
        """Load trusted accounts from JSON file as a set for O(1) lookup"""
        try:
            with open('trusted_accounts.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                accounts = data.get('trusted_usernames', [])
                print(f"✅ Loaded {len(accounts)} trusted accounts")
                # Return a set for O(1) lookup efficiency
                return set(account.lower().strip() for account in accounts)
        except FileNotFoundError:
            print("⚠️  trusted_accounts.json not found - creating example file")
            self.create_example_trusted_file()
            return set()
        except Exception as e:
            print(f"❌ Error loading trusted accounts: {e}")
            return set()
    
    def create_example_trusted_file(self):
        """Create example trusted accounts file"""
        example_data = {
            "trusted_usernames": [
                "best_friend",
                "family_member",
                "work_account", 
                "important_brand"
            ],
            "description": "Add usernames (without @) that you want to keep following"
        }
        
        with open('trusted_accounts.json', 'w', encoding='utf-8') as f:
            json.dump(example_data, f, indent=2, ensure_ascii=False)
        
        print("📝 Created trusted_accounts.json - edit it before running the script!")
    
    async def human_delay(self, min_sec=1, max_sec=3):
        """Add human-like random delays"""
        delay = random.uniform(min_sec, max_sec)
        await asyncio.sleep(delay)
    
    async def start_browser(self):
        """Initialize Playwright browser with stealth settings"""
        print("🚀 Starting browser...")
        
        try:
            # Close any existing browser first
            await self.close_browser()
            
            self.playwright = await async_playwright().start()
            
            # Choose browser based on type and mode
            if self.browser_type == "firefox":
                print("🦊 Using Firefox browser")
                browser_instance = self.playwright.firefox
            elif self.browser_type == "webkit":
                print("🧭 Using WebKit browser")
                browser_instance = self.playwright.webkit
            else:  # chromium
                print("🌐 Using Chromium browser")
                browser_instance = self.playwright.chromium
            
            # Launch browser
            if not self.headless and self.browser_type == "chromium":
                print("⚠️  Chromium GUI mode may be unstable on this system")
                print("🔄 Trying Chromium with enhanced stability settings...")
                
                try:
                    self.browser = await browser_instance.launch(
                        headless=False,
                        args=['--no-sandbox'],
                        slow_mo=100
                    )
                except Exception as e:
                    print(f"❌ Chromium GUI failed: {e}")
                    print("🔄 Falling back to headless mode...")
                    self.headless = True
                    self.browser = await browser_instance.launch(
                        headless=True,
                        args=['--no-sandbox', '--disable-dev-shm-usage']
                    )
            else:
                # Firefox/WebKit or headless mode
                launch_args = {}
                if self.browser_type == "chromium":
                    launch_args["args"] = ['--no-sandbox', '--disable-dev-shm-usage']
                
                self.browser = await browser_instance.launch(
                    headless=self.headless,
                    **launch_args
                )
            
            # Create context with appropriate user agent
            if self.browser_type == "firefox":
                user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:119.0) Gecko/20100101 Firefox/119.0'
            elif self.browser_type == "webkit":
                user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
            else:
                user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            
            self.context = await self.browser.new_context(
                user_agent=user_agent,
                viewport={'width': 1366, 'height': 768},
                ignore_https_errors=True
            )
            
            # Add small delay before creating page
            await asyncio.sleep(0.5)
            
            # Create page
            self.page = await self.context.new_page()
            
            # Set default timeouts
            self.page.set_default_timeout(30000)
            self.page.set_default_navigation_timeout(30000)
            
            mode = "headless" if self.headless else "GUI"
            print(f"✅ {self.browser_type.title()} browser started successfully ({mode} mode)")
            
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            await self.close_browser()
            raise
    
    async def login_to_instagram(self):
        """Login to Instagram with human-like behavior"""
        print("🔐 Logging into Instagram...")
        
        try:
            # Navigate to Instagram
            await self.page.goto('https://www.instagram.com/accounts/login/', wait_until='networkidle', timeout=30000)
            await self.human_delay(2, 4)
            
            # Wait for and fill username
            print("📝 Filling username...")
            username_input = await self.page.wait_for_selector('input[name="username"]', timeout=10000)
            await username_input.click()
            await self.human_delay(0.5, 1)
            await username_input.fill(self.username)
            
            await self.human_delay(0.5, 1)
            
            # Fill password
            print("📝 Filling password...")
            password_input = await self.page.wait_for_selector('input[name="password"]')
            await password_input.click()
            await self.human_delay(0.3, 0.7)
            await password_input.fill(self.password)
            
            await self.human_delay(1, 2)
            
            # Click login button
            print("🔑 Clicking login...")
            login_button = await self.page.wait_for_selector('button[type="submit"]')
            await login_button.click()
            
            print("⏳ Waiting for login...")
            await self.human_delay(5, 8)
            
            # Check if login was successful
            try:
                # Look for home page indicators or profile elements
                await self.page.wait_for_selector(
                    'svg[aria-label="Home"], svg[aria-label="Inicio"], [role="main"], nav[role="navigation"]', 
                    timeout=15000
                )
                print("✅ Login successful!")
                return True
                
            except:
                # Check for error messages
                try:
                    error_element = await self.page.wait_for_selector(
                        '[data-testid="login-error-message"], .eiCW- span, #slfErrorAlert', 
                        timeout=2000
                    )
                    error_text = await error_element.text_content()
                    print(f"❌ Login failed: {error_text}")
                except:
                    print("❌ Login failed: Could not determine error")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    async def navigate_to_following(self):
        """Navigate to profile and click on following button to open modal"""
        print("📋 Navigating to following list...")
        
        try:
            # First, go to the user's profile page
            profile_url = f"https://www.instagram.com/{self.username}/"
            print(f"🔗 Going to profile: {profile_url}")
            
            await self.page.goto(profile_url, wait_until='networkidle', timeout=30000)
            await self.human_delay(2, 4)
            
            # Look for the following/seguidos link/button and click it
            print("🔍 Looking for following/seguidos button...")
            
            # Multiple selectors to try for the following button
            following_selectors = [
                f'a[href="/{self.username}/following/"]',
                'a[href*="/following/"]',
                'text=seguidos',
                'text=following',
                # Try with spans that contain the text
                'span:has-text("seguidos")',
                'span:has-text("following")',
                # Try with div elements that might contain the text
                'div:has-text("seguidos")',
                'div:has-text("following")',
                # More specific selectors
                '[data-testid="following"]',
                'a[role="link"]:has-text("seguidos")',
                'a[role="link"]:has-text("following")'
            ]
            
            following_clicked = False
            
            for i, selector in enumerate(following_selectors):
                try:
                    print(f"   Trying selector {i+1}: {selector}")
                    
                    # Wait a bit longer for the element
                    following_element = await self.page.wait_for_selector(selector, timeout=5000)
                    
                    if following_element:
                        # Check if element is visible and clickable
                        is_visible = await following_element.is_visible()
                        if is_visible:
                            print(f"   ✅ Found visible following element with selector: {selector}")
                            
                            # Scroll element into view
                            await following_element.scroll_into_view_if_needed()
                            await self.human_delay(0.5, 1)
                            
                            # Click the element
                            await following_element.click()
                            print("✅ Clicked following button")
                            following_clicked = True
                            break
                        else:
                            print(f"   ⚠️  Element found but not visible")
                    
                except Exception as e:
                    print(f"   ❌ Selector {i+1} failed: {str(e)[:50]}...")
                    continue
            
            if not following_clicked:
                print("❌ Could not find or click following button")
                
                # Try a different approach - look for any element containing numbers (followers/following)
                print("🔄 Trying alternative approach - looking for profile stats...")
                try:
                    # Look for profile stats section
                    stats_elements = await self.page.query_selector_all('a[href*="/following/"], a[href*="/followers/"]')
                    
                    for element in stats_elements:
                        href = await element.get_attribute('href')
                        if href and '/following/' in href:
                            print("✅ Found following link in profile stats")
                            await element.scroll_into_view_if_needed()
                            await self.human_delay(0.5, 1)
                            await element.click()
                            print("✅ Clicked following link from stats")
                            following_clicked = True
                            break
                            
                except Exception as e:
                    print(f"❌ Alternative approach failed: {e}")
            
            if not following_clicked:
                print("❌ Could not access following list through profile")
                return False
            
            # Wait for the modal to appear
            print("⏳ Waiting for following modal to open...")
            await self.human_delay(2, 4)
            
            try:
                # Wait for the modal dialog
                await self.page.wait_for_selector('[role="dialog"]', timeout=15000)
                print("✅ Following modal opened successfully")
                
                # Additional check - make sure we can see user containers
                await self.human_delay(1, 2)
                user_containers = await self.page.query_selector_all('[role="dialog"] div')
                print(f"📊 Modal contains {len(user_containers)} elements")
                
                return True
                
            except Exception as e:
                print(f"❌ Modal did not open: {e}")
                
                # Try to check if we're on a following page instead of modal
                current_url = self.page.url
                if '/following/' in current_url:
                    print("✅ On following page (not modal, but acceptable)")
                    return True
                
                return False
            
        except Exception as e:
            print(f"❌ Error navigating to following: {e}")
            return False
    
    async def extract_username_from_element(self, user_element):
        """Extract username from user element"""
        try:
            # Validate that user_element is a proper Playwright element
            if not user_element or not hasattr(user_element, 'query_selector'):
                return None
                
            # Try different selectors for username
            username_selectors = [
                'span._ap3a._aaco._aacw._aacx._aad7._aade',
                'a[href*="/"] span[dir="auto"]',
                '.notranslate',
                'a[role="link"] span',
                'span[title]',
                'a span:first-child'
            ]
            
            for selector in username_selectors:
                try:
                    username_elem = await user_element.query_selector(selector)
                    if username_elem:
                        username = await username_elem.text_content()
                        if username and username.strip() and not username.isspace():
                            # Clean the username
                            clean_username = username.strip().replace('@', '')
                            if clean_username and len(clean_username) > 0:
                                return clean_username
                except Exception as e:
                    continue
            
            return None
            
        except Exception as e:
            print(f"⚠️  Error extracting username: {str(e)[:50]}...")
            return None
    
    async def find_unfollow_button(self, user_element):
        """Find the unfollow button for a user"""
        try:
            # Validate that user_element is a proper Playwright element
            if not user_element or not hasattr(user_element, 'query_selector'):
                return None
                
            # Look for "Siguiendo" or "Following" button
            button_selectors = [
                'button:has-text("Siguiendo")',
                'button:has-text("Following")',
                'button[class*="_acan _acap _acas _aj1-"]',
                'button[class*="_acan _acap _acat _aj1-"]',
                'button[type="button"]:has-text("Siguiendo")',
                'button[type="button"]:has-text("Following")'
            ]
            
            for selector in button_selectors:
                try:
                    button = await user_element.query_selector(selector)
                    if button:
                        # Check if button is actually visible and clickable
                        is_visible = await button.is_visible()
                        if is_visible:
                            return button
                except Exception as e:
                    continue
            
            return None
            
        except Exception as e:
            print(f"⚠️  Error finding unfollow button: {str(e)[:50]}...")
            return None
    
    async def process_unfollow_list(self):
        """Process the following list and unfollow users in real-time"""
        print(f"\n🎯 Starting real-time unfollow process")
        
        unfollowed_count = 0
        protected_count = 0
        errors = 0
        processed_users = set()
        
        try:
            # Check if we have a modal or are on a following page
            is_modal = False
            try:
                await self.page.wait_for_selector('[role="dialog"]', timeout=5000)
                is_modal = True
                print("✅ Working with modal interface")
                await self.human_delay(2, 3)
            except:
                # Check if we're on a following page
                current_url = self.page.url
                if '/following/' in current_url:
                    print("✅ Working with following page interface")
                    await self.human_delay(2, 3)
                else:
                    print("❌ Not on following page or modal")
                    return
            
            consecutive_no_new_users = 0
            max_scroll_attempts = 5
            
            while consecutive_no_new_users < max_scroll_attempts:
                # Get current user containers
                user_containers = await self.get_user_containers(is_modal)
                
                if not user_containers:
                    print("❌ No user containers found")
                    break
                
                new_users_found = False
                
                # Process each container immediately
                for container in user_containers:
                    try:
                        # Validate container element
                        if not container or isinstance(container, dict):
                            continue
                        
                        # Check if element is still valid
                        try:
                            await container.is_visible()
                        except Exception:
                            continue
                        
                        # Extract username
                        username = await self.extract_username_from_element(container)
                        
                        if not username or username in processed_users:
                            continue
                        
                        processed_users.add(username)
                        new_users_found = True
                        
                        print(f"\n👤 Processing: @{username}")
                        
                        # Check if user is trusted (O(1) lookup with set)
                        if username.lower() in self.trusted_accounts:
                            print(f"🛡️  PROTECTED: @{username}")
                            protected_count += 1
                            continue
                        
                        # Find and click unfollow button immediately
                        success = await self.unfollow_user(container, username)
                        
                        if success:
                            unfollowed_count += 1
                            print(f"✅ Unfollowed: @{username}")
                            # Delay after successful unfollow
                            await self.human_delay(3, 6)
                        else:
                            errors += 1
                        
                        # Small delay between users
                        await self.human_delay(1, 2)
                        
                    except Exception as e:
                        print(f"❌ Error processing user: {str(e)[:100]}...")
                        errors += 1
                        continue
                
                # Handle scrolling if no new users found
                if not new_users_found:
                    consecutive_no_new_users += 1
                    print(f"📜 No new users found, scrolling... (attempt {consecutive_no_new_users}/{max_scroll_attempts})")
                    
                    # Store count before scroll
                    containers_before = len(user_containers)
                    
                    scroll_success = await self.scroll_for_more_users(is_modal)
                    if not scroll_success:
                        print("❌ Could not scroll, stopping")
                        break
                    
                    # Wait for new content to load
                    print("⏳ Waiting for new content to load...")
                    await self.human_delay(3, 5)
                    
                    # Check if new containers appeared
                    new_containers = await self.get_user_containers(is_modal)
                    containers_after = len(new_containers)
                    
                    print(f"📊 Containers before scroll: {containers_before}, after: {containers_after}")
                    
                    if containers_after > containers_before + 2:  # Some tolerance for dynamic content
                        print(f"✅ Found {containers_after - containers_before} new containers!")
                        consecutive_no_new_users = 0  # Reset counter
                    else:
                        print("⚠️  No significant new content loaded")
                else:
                    consecutive_no_new_users = 0
                
                # Safety check
                if errors > 10:
                    print("⚠️  Too many errors, stopping")
                    break
            
            print(f"\n🎉 PROCESS COMPLETED")
            print(f"   • Unfollowed: {unfollowed_count}")
            print(f"   • Protected: {protected_count}")
            print(f"   • Errors: {errors}")
            print(f"   • Total processed: {len(processed_users)}")
            
        except Exception as e:
            print(f"❌ Error in unfollow process: {e}")
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")
            print(f"   • Processed {len(processed_users)} users before error")
            print(f"   • Unfollowed: {unfollowed_count}")
            print(f"   • Protected: {protected_count}")
            print(f"   • Errors: {errors}")
    
    async def get_user_containers(self, is_modal):
        """Get user containers based on interface type"""
        user_containers = []
        
        if is_modal:
            # Try main modal selector first
            try:
                user_containers = await self.page.query_selector_all(
                    '[role="dialog"] div[class*="x1dm5mii x16mil14 xi81zsa x1yutycm x1lliihq x193iq5w xh8yej3"]'
                )
            except Exception:
                pass
            
            # Try alternative selectors if needed
            if not user_containers:
                alternative_selectors = [
                    '[role="dialog"] div:has(button:has-text("Following"))',
                    '[role="dialog"] div:has(button:has-text("Siguiendo"))',
                    '[role="dialog"] > div > div > div > div'
                ]
                
                for selector in alternative_selectors:
                    try:
                        user_containers = await self.page.query_selector_all(selector)
                        if user_containers:
                            break
                    except Exception:
                        continue
        else:
            # Page selectors
            try:
                user_containers = await self.page.query_selector_all(
                    'div:has(button:has-text("Following")), div:has(button:has-text("Siguiendo"))'
                )
            except Exception:
                pass
        
        return user_containers
    
    async def unfollow_user(self, container, username):
        """Unfollow a specific user immediately"""
        try:
            # Find unfollow button
            unfollow_button = await self.find_unfollow_button(container)
            
            if not unfollow_button:
                print(f"⚠️  No unfollow button found for @{username}")
                return False
            
            # Validate button is still clickable
            try:
                await unfollow_button.is_visible()
                await unfollow_button.is_enabled()
            except Exception:
                print(f"⚠️  Button invalid for @{username}")
                return False
            
            # Click unfollow button
            await unfollow_button.click()
            await self.human_delay(0.5, 1)
            
            # Handle confirmation dialog
            try:
                confirm_button = await self.page.wait_for_selector(
                    'button:has-text("Dejar de seguir"), button:has-text("Unfollow")',
                    timeout=3000
                )
                await confirm_button.click()
                return True
                
            except Exception:
                print(f"⚠️  Could not confirm unfollow for @{username}")
                return False
                
        except Exception as e:
            print(f"⚠️  Error unfollowing @{username}: {str(e)[:50]}...")
            return False
    
    async def scroll_for_more_users(self, is_modal):
        """Scroll to load more users with better verification"""
        try:
            if is_modal:
                # Modal scrolling with verification
                print("🔄 Scrolling modal down...")
                try:
                    # Get current scroll position
                    before_scroll = await self.page.evaluate('document.querySelector(\'[role="dialog"]\').scrollTop')
                    print(f"   Before scroll: {before_scroll}")
                    
                    # Try multiple scrolling methods
                    # Method 1: Scroll down incrementally
                    await self.page.evaluate('document.querySelector(\'[role="dialog"]\').scrollTop += 2000')
                    await asyncio.sleep(1)
                    
                    # Method 2: Scroll to bottom
                    await self.page.evaluate('document.querySelector(\'[role="dialog"]\').scrollTop = document.querySelector(\'[role="dialog"]\').scrollHeight')
                    await asyncio.sleep(1)
                    
                    # Method 3: Use mouse wheel on modal
                    try:
                        modal = await self.page.wait_for_selector('[role="dialog"]', timeout=2000)
                        if modal:
                            box = await modal.bounding_box()
                            if box:
                                # Move mouse to center of modal
                                await self.page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
                                # Multiple wheel scrolls
                                for i in range(10):
                                    await self.page.mouse.wheel(0, 300)
                                    await asyncio.sleep(0.2)
                    except Exception as wheel_error:
                        print(f"   ⚠️  Mouse wheel failed: {wheel_error}")
                    
                    # Check final position
                    after_scroll = await self.page.evaluate('document.querySelector(\'[role="dialog"]\').scrollTop')
                    print(f"   After scroll: {after_scroll}")
                    
                    # Verify scroll worked
                    if after_scroll > before_scroll:
                        print("   ✅ Modal scrolled successfully")
                        return True
                    else:
                        print("   ⚠️  Modal did not scroll - trying alternative method")
                        
                        # Alternative: Use keyboard
                        try:
                            await self.page.keyboard.press('End')
                            await asyncio.sleep(1)
                            await self.page.keyboard.press('PageDown')
                            await asyncio.sleep(1)
                            return True
                        except Exception:
                            print("   ❌ Keyboard scroll also failed")
                            return False
                        
                except Exception as e:
                    print(f"   ❌ Modal scroll failed: {e}")
                    return False
            else:
                # Page scrolling with verification
                print("🔄 Scrolling page down...")
                try:
                    before_y = await self.page.evaluate('window.pageYOffset')
                    print(f"   Before scroll: {before_y}")
                    
                    # Multiple scroll methods
                    await self.page.evaluate('window.scrollBy(0, 2000)')
                    await asyncio.sleep(1)
                    await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    await asyncio.sleep(1)
                    
                    # Mouse wheel as backup
                    for i in range(5):
                        await self.page.mouse.wheel(0, 500)
                        await asyncio.sleep(0.3)
                    
                    after_y = await self.page.evaluate('window.pageYOffset')
                    print(f"   After scroll: {after_y}")
                    
                    if after_y > before_y:
                        print("   ✅ Page scrolled successfully")
                        return True
                    else:
                        print("   ⚠️  Page did not scroll")
                        return False
                        
                except Exception as e:
                    print(f"   ❌ Page scroll failed: {e}")
                    return False
        except Exception as e:
            print(f"❌ Scroll function error: {e}")
            return False

    async def close_browser(self):
        """Close browser safely"""
        try:
            if self.page:
                await self.page.close()
                self.page = None
                print("📄 Page closed")
        except Exception as e:
            print(f"⚠️  Error closing page: {e}")
        
        try:
            if self.context:
                await self.context.close()
                self.context = None
                print("🔗 Context closed")
        except Exception as e:
            print(f"⚠️  Error closing context: {e}")
        
        try:
            if self.browser:
                await self.browser.close()
                self.browser = None
                print("🌐 Browser closed")
        except Exception as e:
            print(f"⚠️  Error closing browser: {e}")
        
        try:
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
                print("🎭 Playwright stopped")
        except Exception as e:
            print(f"⚠️  Error stopping playwright: {e}")

async def main():
    print("🔥 Instagram Playwright Unfollow Bot")
    print("="*45)
    print("⚠️  This script uses browser automation to unfollow Instagram users")
    print("   while protecting accounts in your trusted list.")
    print()
    
    # Check Playwright installation first
    if not await check_playwright_installation():
        print("\n❌ Playwright is not properly set up. Please fix the installation and try again.")
        return
    
    # Get user input
    username = input("📱 Instagram Username: ").strip()
    password = input("🔒 Password: ").strip()
    
    if not username or not password:
        print("❌ Username and password are required!")
        return
    
    # Ask about browser choice
    print("\n🌐 Choose your browser:")
    print("1. Firefox (🦊 - Recommended, stable GUI)")
    print("2. WebKit/Safari (🧭 - Good alternative)")  
    print("3. Chromium (🌐 - May have GUI issues on macOS)")
    
    browser_choice = input("Enter choice (1/2/3, default 1): ").strip() or "1"
    
    browser_map = {
        "1": "firefox",
        "2": "webkit", 
        "3": "chromium"
    }
    browser_type = browser_map.get(browser_choice, "firefox")
    
    # Ask about headless mode
    headless_choice = input("🖥️  Use GUI mode to see what happens? (Y/n): ").strip().lower()
    headless = headless_choice == 'n'
    
    # Create bot instance
    bot = InstagramPlaywrightBot(username, password, headless=headless, browser_type=browser_type)
    
    try:
        # Start browser
        await bot.start_browser()
        
        # Login
        if not await bot.login_to_instagram():
            print("❌ Login failed. Exiting...")
            return
        
        # Navigate to following list
        if not await bot.navigate_to_following():
            print("❌ Could not access following list. Exiting...")
            return
        
        # Ask for final confirmation before starting
        print(f"\n" + "="*45)
        print("⚠️  This will start REAL unfollowing immediately!")
        print("   Only accounts in your trusted_accounts.json will be protected.")
        proceed = input("🚨 Do you want to proceed? (type 'YES'): ").strip()
        
        if proceed == 'YES':
            print(f"\n🚀 Starting real-time unfollow process...")
            await bot.process_unfollow_list()
        else:
            print("✅ Process cancelled by user")
        
        if not headless:
            input("\n🏁 Press Enter to close browser...")
        
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Always try to close browser safely
        await bot.close_browser()

if __name__ == "__main__":
    asyncio.run(main())