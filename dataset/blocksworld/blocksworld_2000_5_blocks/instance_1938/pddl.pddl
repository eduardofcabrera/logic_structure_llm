

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b a)
(on c d)
(ontable d)
(ontable e)
(clear b)
(clear e)
)
(:goal
(and
(on a e)
(on d c)
(on e d))
)
)


