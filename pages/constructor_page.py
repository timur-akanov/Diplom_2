from .base_page import BasePage
from .locators import IngredientLocators, OrderLocators, ConstructorLocators
from selenium.webdriver.common.by import By
import time


class ConstructorPage(BasePage):
    def open_ingredient(self):
        # Use BasePage.click to wait for clickable and handle overlays
        self.click(IngredientLocators.INGREDIENT_CARD)

    def drag_ingredient_to_constructor(self):
        tgt = self.find(ConstructorLocators.BASKET)
        # Use JS-based drag and drop; choose first ingredient card not inside a modal
        self.driver.execute_script("""
        const tgt = arguments[0];
        const selector = '[class*="BurgerIngredient_ingredient__"], [class*="ingredient__"]';
        const nodes = Array.from(document.querySelectorAll(selector));
        let src = null;
        for (const n of nodes) {
            // skip elements that are inside a modal overlay/container
            if (!n.closest('[class*="Modal_modal__container"], [class*="modal"]')) {
                src = n;
                break;
            }
        }
        if (!src && nodes.length) src = nodes[0];
        const rect = src.getBoundingClientRect();
        const dataTransfer = new DataTransfer();
        function triggerDrag(el, type, clientX, clientY) {
            const ev = new DragEvent(type, {
                bubbles: true,
                cancelable: true,
                clientX: clientX,
                clientY: clientY,
                dataTransfer: dataTransfer
            });
            el.dispatchEvent(ev);
        }
        triggerDrag(src, 'dragstart', rect.x+5, rect.y+5);
        const rectT = tgt.getBoundingClientRect();
        triggerDrag(tgt, 'dragenter', rectT.x+5, rectT.y+5);
        triggerDrag(tgt, 'dragover', rectT.x+5, rectT.y+5);
        triggerDrag(tgt, 'drop', rectT.x+5, rectT.y+5);
        triggerDrag(src, 'dragend', rect.x+5, rect.y+5);
        """, tgt)
        time.sleep(0.5)

    def close_modal(self):
        self.click(IngredientLocators.MODAL_CLOSE)

    def add_to_order(self):
        # Try clicking the modal's add button and wait for the ingredient counter to increase.
        try:
            self.click(IngredientLocators.ADD_TO_ORDER)
            # wait briefly for counter update
            import time
            end = time.time() + 5
            while time.time() < end:
                try:
                    card = self.find(IngredientLocators.INGREDIENT_CARD)
                    cnt = self.get_counter(card)
                    if cnt and cnt != '0':
                        return
                except Exception:
                    pass
                time.sleep(0.2)
            # if counter didn't update, try a JS click as fallback
            try:
                el = self.find(IngredientLocators.ADD_TO_ORDER)
                self.driver.execute_script('arguments[0].click();', el)
            except Exception:
                # as a last resort perform drag-and-drop
                self.drag_ingredient_to_constructor()
        except Exception:
            # fallback to drag-and-drop into constructor
            self.drag_ingredient_to_constructor()

    def get_counter(self, card_element):
        try:
            return card_element.find_element(*IngredientLocators.COUNTER).text
        except Exception:
            return '0'
