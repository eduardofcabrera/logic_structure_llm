

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b c)
(ontable c)
(ontable d)
(on e d)
(clear a)
(clear b)
)
(:goal
(and
(on a b)
(on b d)
(on d e))
)
)


