

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(on c a)
(on d c)
(ontable e)
(clear b)
(clear d)
)
(:goal
(and
(on a c)
(on b d)
(on e a))
)
)


