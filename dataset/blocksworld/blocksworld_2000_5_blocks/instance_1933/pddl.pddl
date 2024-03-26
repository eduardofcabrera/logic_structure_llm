

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(ontable c)
(on d c)
(on e a)
(clear b)
(clear e)
)
(:goal
(and
(on b d)
(on c e))
)
)


